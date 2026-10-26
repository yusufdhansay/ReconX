# ReconX

> Automated Recon Framework for Pentesters

ReconX automates the first phase of penetration testing: Reconnaissance and OSINT.
Give it a domain and it enumerates subdomains, scans ports, fingerprints the tech
stack, harvests OSINT emails, and generates a report.

## Status

Work in progress. Built in phases:

1. CLI, banner, project structure
2. Subdomain enumeration + WHOIS lookup
3. Port scanning + tech stack detection
4. Email harvesting OSINT
5. HTML + JSON report generation

## Installation

```bash
git clone https://github.com/yusufdhansay/ReconX.git
cd ReconX
pip install -r requirements.txt
```

## Usage

```bash
python reconx.py --domain example.com --output reports/
```

## Legal Disclaimer

ReconX is for educational purposes and authorized security testing only.
Use it only on targets you own or have explicit written permission to test.
The authors take no responsibility for misuse.
