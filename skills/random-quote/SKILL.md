---
name: random-quote
description: "Fetch one random quote from the ZenQuotes API, translate it into German, and return the German version, formatted, with nothing else. Use this skill whenever the user says \"random quote\", \"give me a quote\", \"quote of the day\", \"inspire me\", \"motivational quote\", asks for an inspirational or motivational line, or invokes /random-quote. Always fetch a live quote — never write one from memory.\n"
---

# Random Quote

Fetch a single random quote from ZenQuotes and hand it back. The point of this skill is that the
quote is real and comes from the API, so a made-up or remembered quote is never an acceptable
substitute, even when the service is down.

## Steps

1. **Call the API from the shell** with a 5-second timeout:

   ```bash
   curl -sS --max-time 5 https://zenquotes.io/api/random
   ```

   (`GET`, no API key.)

2. **If the shell can't reach the site** — a proxy 403, a blocked network, a TLS/connection error
   or a timeout — try the same URL **once** with WebFetch, asking it to return the raw JSON.
   Don't try any other workaround (no other tools, mirrors, caches or alternative quote sites).

3. **Read the response.** It is a JSON array holding one object:
   - `q` — the quote
   - `a` — the author
   - `h` — an HTML version; ignore it.

4. **Translate the quote into German.** Translate `q` faithfully and naturally, keeping the
   meaning, tone and punchiness of the original. Keep the author's name as returned in `a`
   (do not translate names). If the author is `zenquotes.io` (rate-limit case, see Errors),
   do not translate; follow the Errors section instead.

5. **Reply with only the German quote**, in this format:

   ```
   > *„<German q>"*
   > — <a>
   ```

   Use German quotation marks („…"). Do not include the original English text.

   No introduction, commentary or follow-up unless the user asks for it.

## Errors

- **Rate limit.** The free tier allows only a few calls per 30 seconds. When it is exceeded the
  API still returns a normal-looking object whose `q` is a "Too many requests" message (and the
  author may read "zenquotes.io"). Treat that as a rate limit, not a quote: tell the user to try
  again in a moment. Don't retry, and never loop.

- **Blocked or failed** (both curl and the single WebFetch attempt failed, or the response isn't
  the expected JSON): say the quote service couldn't be reached, show the error briefly (one
  line, e.g. the HTTP status or curl message), and remind the user that `zenquotes.io` must be on
  the organisation's network allowlist — **Organization settings → Capabilities → "Package
  managers and specific domains"**. Never invent a quote or use one from memory.

## Attribution

If the user says the quote is going somewhere public — a slide, a post, a newsletter, or similar —
add this line under the quote:

> Inspirational quotes provided by ZenQuotes API (https://zenquotes.io/).

It's a condition of the free API, so include it whenever the quote will be published.
