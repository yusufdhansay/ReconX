"""WHOIS lookup module using python-whois."""

import whois

from utils import logger


def _stringify(value):
    """Normalize WHOIS fields that may be lists or datetimes to strings."""
    if value is None:
        return None
    if isinstance(value, list):
        # Deduplicate while preserving readable order.
        cleaned = [str(v) for v in value if v]
        seen = []
        for item in cleaned:
            if item not in seen:
                seen.append(item)
        return seen
    return str(value)


def lookup(domain):
    """Return a dict of key WHOIS fields. Errors are handled gracefully."""
    logger.info("Running WHOIS lookup...")

    result = {
        "domain": domain,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "name_servers": None,
        "error": None,
    }

    try:
        data = whois.whois(domain)
    except Exception as exc:
        logger.warn(f"WHOIS lookup failed: {exc}")
        result["error"] = str(exc)
        return result

    result["registrar"] = _stringify(data.get("registrar"))
    result["creation_date"] = _stringify(data.get("creation_date"))
    result["expiration_date"] = _stringify(data.get("expiration_date"))
    result["name_servers"] = _stringify(data.get("name_servers"))

    if result["registrar"]:
        logger.success(f"Registrar: {result['registrar']}")
    else:
        logger.warn("WHOIS returned no registrar (may be privacy protected)")

    return result
