"""Companies House API client: Public Data API, Document API and Streaming API.

Auth is HTTP Basic with the API key as the username and an empty password. The key is
read from CH_API_KEY. The key allows 600 requests per 5 minutes; a 429 is retried after
the window given in X-Ratelimit-Reset.
"""
import json
import os
import time

import requests

API_BASE = "https://api.company-information.service.gov.uk"
DOCUMENT_BASE = "https://document-api.company-information.service.gov.uk"
STREAM_BASE = "https://stream.companieshouse.gov.uk"

PAGE_SIZE = 100
TOTAL_KEYS = ("total_results", "total_count", "hits")
PSC_KINDS = (
    "corporate-entity-beneficial-owner",
    "corporate-entity",
    "individual-beneficial-owner",
    "individual",
    "legal-person-beneficial-owner",
    "legal-person",
    "super-secure-beneficial-owner",
    "super-secure",
)
STREAM_RESOURCES = (
    "companies",
    "filings",
    "officers",
    "persons-with-significant-control",
    "charges",
    "insolvency-cases",
)
RETRY_STATUSES = (429, 500, 502, 503, 504)


class CHError(Exception):
    pass


def normalise_number(value):
    """'445790' -> '00445790'; 'sc123456' -> 'SC123456'."""
    number = value.strip().upper().replace(" ", "")
    if number.isdigit() and len(number) < 8:
        number = number.zfill(8)
    return number


def document_id(ref):
    """Accepts a bare document id or the document_metadata URL from a filing-history item."""
    return ref.rstrip("/").split("/")[-1]


class CH:
    def __init__(self, key=None, timeout=30, max_retries=4):
        key = (key or os.environ.get("CH_API_KEY", "")).strip()
        if not key:
            raise CHError("CH_API_KEY is not set in the environment.")
        self.session = requests.Session()
        self.session.auth = (key, "")
        self.timeout = timeout
        self.max_retries = max_retries
        self.calls = 0

    @staticmethod
    def _wait(resp, attempt):
        if resp.status_code == 429:
            reset = resp.headers.get("X-Ratelimit-Reset", "")
            if reset.isdigit():
                return min(max(int(reset) - int(time.time()) + 1, 1), 600)
            return 60
        return 2 ** attempt

    def _send(self, url, params=None, accept=None, stream=False):
        headers = {"Accept": accept} if accept else {}
        for attempt in range(self.max_retries + 1):
            self.calls += 1
            resp = self.session.get(
                url, params=params, headers=headers, timeout=self.timeout, stream=stream
            )
            if attempt < self.max_retries and resp.status_code in RETRY_STATUSES:
                time.sleep(self._wait(resp, attempt))
                continue
            return resp

    def _json(self, url, params=None, allow_404=False):
        resp = self._send(url, params)
        if resp.status_code == 404 and allow_404:
            return None
        if resp.status_code >= 400:
            raise CHError(f"HTTP {resp.status_code} from {url}: {resp.text[:300]}")
        return resp.json()

    def get(self, path, params=None, allow_404=False):
        """GET a Public Data API path such as /company/00445790. None on 404 when allow_404."""
        return self._json(API_BASE + path, params, allow_404)

    def paged(self, path, params=None, allow_404=False, limit=None):
        """Read every page of a list endpoint and return the first page with all items merged."""
        query = dict(params or {})
        query["items_per_page"] = PAGE_SIZE
        items, head, start = [], None, 0
        while limit is None or len(items) < limit:
            query["start_index"] = start
            page = self.get(path, query, allow_404)
            if page is None:
                return None
            head = head or page
            batch = page.get("items") or []
            items.extend(batch)
            total = next((page[k] for k in TOTAL_KEYS if k in page), 0)
            start += len(batch)
            if len(batch) < PAGE_SIZE or start >= total:
                break
        result = dict(head)
        result["items"] = items[:limit] if limit else items
        return result

    def document_metadata(self, ref):
        return self._json(f"{DOCUMENT_BASE}/document/{document_id(ref)}")

    def document_content(self, ref, accept="application/pdf"):
        """Returns (bytes, content_type) for a filing document."""
        resp = self._send(f"{DOCUMENT_BASE}/document/{document_id(ref)}/content", accept=accept)
        if resp.status_code >= 400:
            raise CHError(
                f"HTTP {resp.status_code} for document {document_id(ref)}: {resp.text[:300]}"
            )
        return resp.content, resp.headers.get("Content-Type", "")

    def stream(self, resource, timepoint=None, max_events=10):
        """Read up to max_events from a Streaming API resource, then close the connection."""
        params = {"timepoint": timepoint} if timepoint is not None else None
        resp = self._send(f"{STREAM_BASE}/{resource}", params, stream=True)
        if resp.status_code >= 400:
            raise CHError(f"HTTP {resp.status_code} from {STREAM_BASE}/{resource}: {resp.text[:300]}")
        events = []
        try:
            for line in resp.iter_lines(decode_unicode=True):
                if line.strip():
                    events.append(json.loads(line))
                    if len(events) >= max_events:
                        break
        except requests.exceptions.ReadTimeout:
            pass  # no further events arrived within the timeout
        finally:
            resp.close()
        return events
