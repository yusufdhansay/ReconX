"""Fast multi-threaded TCP connect port scanner using sockets."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import logger


# Top 10 common ports with friendly service labels.
TOP_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Proxy",
}

TIMEOUT = 0.5
MAX_WORKERS = 10


def _scan_port(host, port):
    """Return port if a TCP connect succeeds, else None."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        try:
            if sock.connect_ex((host, port)) == 0:
                return port
        except OSError:
            return None
    return None


def scan(domain):
    """Scan the top ports on a host and return a list of open port dicts."""
    logger.info("Scanning top 10 ports...")

    try:
        host = socket.gethostbyname(domain)
    except socket.gaierror as exc:
        logger.warn(f"Could not resolve {domain}: {exc}")
        return []

    open_ports = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_scan_port, host, port): port
            for port in TOP_PORTS
        }
        for future in as_completed(futures):
            port = future.result()
            if port:
                open_ports.append({"port": port, "service": TOP_PORTS[port]})

    open_ports.sort(key=lambda item: item["port"])
    logger.success(f"Found {len(open_ports)} open ports")
    return open_ports
