#!/usr/bin/env python3
"""ReconX - Automated OSINT & Active Recon Framework for Pentesting.

Main CLI entry point. Takes a target domain and runs the recon pipeline.
"""

import argparse
import os
import sys

from utils import logger
from utils.banner import print_banner


def parse_args():
    """Build and parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="reconx.py",
        description="ReconX - Automated OSINT & Active Recon Framework for Pentesting.",
        epilog="Example: python reconx.py --domain example.com --output reports/",
    )
    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain, e.g. example.com",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="reports/",
        help="Output directory for generated reports (default: reports/)",
    )
    return parser.parse_args()


def clean_domain(domain):
    """Strip scheme, paths and whitespace from a user supplied domain."""
    domain = domain.strip().lower()
    for prefix in ("http://", "https://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    domain = domain.split("/")[0]
    return domain


def run(domain, output_dir):
    """Run the recon pipeline for a single domain.

    Modules are wired in across later phases. Phase 1 only validates
    input and prepares the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Target domain: {domain}")
    logger.info(f"Report output directory: {output_dir}")
    logger.warn("Recon modules are not wired in yet (Phase 1 skeleton).")


def main():
    """Program entry point."""
    print_banner()
    args = parse_args()

    domain = clean_domain(args.domain)
    if not domain or "." not in domain:
        logger.error("Invalid domain. Use a value like example.com")
        sys.exit(1)

    try:
        run(domain, args.output)
    except KeyboardInterrupt:
        logger.error("Interrupted by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
