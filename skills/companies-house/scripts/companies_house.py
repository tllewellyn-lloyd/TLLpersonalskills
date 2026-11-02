"""Minimal client for the Companies House Public Data API.

Auth: HTTP Basic, API key as username, blank password.
Set the key in the COMPANIES_HOUSE_API_KEY environment variable.
Rate limit: 600 requests per 5 minutes per key (HTTP 429 when exceeded).
"""
import os
import sys
import time
from pathlib import Path

import requests

BASE_URL = "https://api.company-information.service.gov.uk"
KEY_FILE = Path(__file__).with_name("api_key.txt")


def _windows_user_env(name):
    """Read a variable saved with setx, which running shells don't see until restarted."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, name)[0]
    except (ImportError, OSError):
        return None


def _rate_limit_wait(response, attempt):
    """Seconds to wait after a 429: until X-Ratelimit-Reset (epoch seconds), else a growing backoff."""
    reset = response.headers.get("X-Ratelimit-Reset", "")
    if reset.isdigit():
        return min(max(int(reset) - int(time.time()) + 1, 1), 330)
    return min(2 ** attempt * 10, 330)


class CompaniesHouse:
    def __init__(self, api_key=None):
        api_key = api_key or os.environ.get("COMPANIES_HOUSE_API_KEY") or _windows_user_env("COMPANIES_HOUSE_API_KEY")
        if not api_key and KEY_FILE.exists():
            api_key = KEY_FILE.read_text().strip()
        if not api_key:
            raise RuntimeError("Set COMPANIES_HOUSE_API_KEY or create scripts/api_key.txt")
        self.session = requests.Session()
        self.session.auth = (api_key, "")

    def request(self, url, params=None, headers=None, timeout=30):
        """GET with retries. A 429 waits for the rate-limit window to reset; 5xx backs off briefly."""
        for attempt in range(6):
            r = self.session.get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 429:
                time.sleep(_rate_limit_wait(r, attempt))
                continue
            if r.status_code in (500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt * 2)
                continue
            return r
        return r

    def get(self, path, **params):
        r = self.request(BASE_URL + path, params=params)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def _paged(self, path, page_size=100, **params):
        """Yield every item from a paginated endpoint."""
        start = 0
        while True:
            data = self.get(path, items_per_page=page_size, start_index=start, **params)
            items = (data or {}).get("items", [])
            yield from items
            start += len(items)
            if not items or start >= data.get("total_results", data.get("total_count", 0)):
                break

    # Search
    def search_companies(self, q, items_per_page=20):
        return self.get("/search/companies", q=q, items_per_page=items_per_page)

    def search_officers(self, q, items_per_page=20):
        return self.get("/search/officers", q=q, items_per_page=items_per_page)

    # Company
    def company(self, number):
        return self.get(f"/company/{number}")

    def registered_office(self, number):
        return self.get(f"/company/{number}/registered-office-address")

    def officers(self, number):
        return list(self._paged(f"/company/{number}/officers"))

    def filing_history(self, number, category=None):
        params = {"category": category} if category else {}
        return list(self._paged(f"/company/{number}/filing-history", **params))

    def pscs(self, number):
        return list(self._paged(f"/company/{number}/persons-with-significant-control"))

    def charges(self, number):
        return self.get(f"/company/{number}/charges")

    def insolvency(self, number):
        return self.get(f"/company/{number}/insolvency")

    # Officer
    def officer_appointments(self, officer_id):
        return list(self._paged(f"/officers/{officer_id}/appointments"))


if __name__ == "__main__":
    ch = CompaniesHouse()
    query = " ".join(sys.argv[1:]) or "Tern"
    for c in ((ch.search_companies(query) or {}).get("items") or [])[:10]:
        print(f'{c["company_number"]}  {c["company_status"]:<12} {c["title"]}')
