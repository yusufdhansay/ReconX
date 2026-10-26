"""Email harvesting OSINT module.

Fetches the target homepage and a few common pages, then extracts email
addresses with a regex. This stays within ToS (no search engine scraping).
"""

import re

import requests

from utils import logger


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
COMMON_PAGES = ["", "/contact", "/about", "/contact-us", "/about-us"]
HTTP_TIMEOUT = 10
HEADERS = {"User-Agent": "ReconX/1.0"}

# Image and asset extensions sometimes match the regex via filenames.
_FALSE_POSITIVE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")


def _fetch(url):
    """GET a URL, returning text or None on failure."""
    try:
        resp = requests.get(url, timeout=HTTP_TIMEOUT, headers=HEADERS)
        if resp.status_code < 400:
            return resp.text
    except requests.RequestException:
        return None
    return None


def _base_url(domain):
    """Return a reachable base URL (https preferred)."""
    for scheme in ("https://", "http://"):
        if _fetch(f"{scheme}{domain}") is not None:
            return f"{scheme}{domain}"
    return None


def _clean(emails):
    """Drop obvious false positives like image filenames."""
    cleaned = set()
    for email in emails:
        low = email.lower()
        if low.endswith(_FALSE_POSITIVE_SUFFIXES):
            continue
        cleaned.add(low)
    return cleaned


def harvest(domain):
    """Scrape common pages for email addresses and return a sorted list."""
    logger.info("Harvesting emails (OSINT)...")

    base = _base_url(domain)
    if base is None:
        logger.warn("Website not reachable, skipping email OSINT")
        return []

    emails = set()
    for page in COMMON_PAGES:
        html = _fetch(base + page)
        if not html:
            continue
        emails |= set(EMAIL_REGEX.findall(html))

    emails = sorted(_clean(emails))
    logger.success(f"Found {len(emails)} email(s)")
    return emails
