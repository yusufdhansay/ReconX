"""Subdomain enumeration module.

Two techniques are combined:

1. Certificate Transparency logs via the public crt.sh JSON API (no key).
2. A small dictionary brute-force resolved with dnspython.
"""

import requests
import dns.resolver

from utils import logger


# Small built-in wordlist for the brute-force pass.
WORDLIST = [
    "www", "mail", "ftp", "admin", "api",
    "dev", "test", "blog", "shop", "staging",
]

CRTSH_URL = "https://crt.sh/?q=%.{domain}&output=json"
HTTP_TIMEOUT = 15


def from_crtsh(domain):
    """Query crt.sh certificate transparency logs for subdomains."""
    found = set()
    try:
        resp = requests.get(
            CRTSH_URL.format(domain=domain),
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": "ReconX/1.0"},
        )
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warn(f"crt.sh lookup failed: {exc}")
        return found

    for entry in data:
        name_value = entry.get("name_value", "")
        for name in name_value.splitlines():
            name = name.strip().lower().lstrip("*.")
            if name.endswith(domain):
                found.add(name)
    return found


def from_bruteforce(domain):
    """Resolve a small wordlist of common subdomains via DNS."""
    found = set()
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2.0
    resolver.lifetime = 2.0

    for word in WORDLIST:
        host = f"{word}.{domain}"
        try:
            resolver.resolve(host, "A")
            found.add(host)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                dns.resolver.NoNameservers, dns.exception.Timeout):
            continue
        except Exception:
            continue
    return found


def enumerate_subdomains(domain):
    """Run both techniques and return a sorted unique list of subdomains."""
    logger.info("Finding subdomains (crt.sh + brute-force)...")

    results = set()
    results |= from_crtsh(domain)
    results |= from_bruteforce(domain)

    # Always include the apex domain itself.
    results.add(domain)

    subdomains = sorted(results)
    logger.success(f"Found {len(subdomains)} subdomains")
    return subdomains
