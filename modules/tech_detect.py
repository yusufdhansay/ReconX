"""Lightweight tech stack detection via HTTP headers and HTML.

No external fingerprinting API is used. Detection is simple string matching
over response headers and a few well known paths.
"""

import requests
from bs4 import BeautifulSoup

from utils import logger


HTTP_TIMEOUT = 10
HEADERS = {"User-Agent": "ReconX/1.0"}


def _fetch(url):
    """GET a URL, returning the response or None on failure."""
    try:
        return requests.get(
            url, timeout=HTTP_TIMEOUT, headers=HEADERS, allow_redirects=True
        )
    except requests.RequestException:
        return None


def _base_url(domain):
    """Try HTTPS first, fall back to HTTP."""
    for scheme in ("https://", "http://"):
        resp = _fetch(f"{scheme}{domain}")
        if resp is not None:
            return resp, f"{scheme}{domain}"
    return None, None


def _detect_cms(base, html):
    """Detect common CMS fingerprints."""
    lowered = html.lower()
    if "wp-content" in lowered or "wp-json" in lowered:
        return "WordPress"

    soup = BeautifulSoup(html, "html.parser")
    generator = soup.find("meta", attrs={"name": "generator"})
    if generator and generator.get("content"):
        return generator["content"]

    # Probe well known WordPress paths.
    for path in ("/wp-login.php", "/wp-json"):
        resp = _fetch(base + path)
        if resp is not None and resp.status_code < 400:
            return "WordPress"
    return None


def detect(domain):
    """Return a dict describing detected server, CMS, CDN and headers."""
    logger.info("Detecting technology stack...")

    result = {
        "url": None,
        "server": None,
        "powered_by": None,
        "cms": None,
        "cdn": None,
        "error": None,
    }

    resp, base = _base_url(domain)
    if resp is None:
        logger.warn("Website not reachable over HTTP/HTTPS")
        result["error"] = "unreachable"
        return result

    result["url"] = base
    headers = resp.headers

    result["server"] = headers.get("Server")
    result["powered_by"] = headers.get("X-Powered-By")

    # CDN detection via headers.
    header_blob = " ".join(f"{k}:{v}" for k, v in headers.items()).lower()
    if "cloudflare" in header_blob:
        result["cdn"] = "Cloudflare"
    elif "akamai" in header_blob:
        result["cdn"] = "Akamai"
    elif "fastly" in header_blob:
        result["cdn"] = "Fastly"

    result["cms"] = _detect_cms(base, resp.text)

    parts = [p for p in (result["server"], result["cms"], result["cdn"]) if p]
    logger.success("Tech: " + (", ".join(parts) if parts else "none detected"))
    return result
