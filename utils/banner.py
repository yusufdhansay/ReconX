"""ASCII banner for ReconX."""

from utils.logger import Colors


BANNER = r"""
  ____                      __  __
 |  _ \ ___  ___ ___  _ __  \ \/ /
 | |_) / _ \/ __/ _ \| '_ \  \  /
 |  _ <  __/ (_| (_) | | | | /  \
 |_| \_\___|\___\___/|_| |_|/_/\_\
"""

TAGLINE = "Automated OSINT & Active Recon Framework for Pentesters"


def print_banner():
    """Print the ReconX ASCII banner with tagline."""
    print(f"{Colors.CYAN}{BANNER}{Colors.RESET}")
    print(f"{Colors.YELLOW}        {TAGLINE}{Colors.RESET}")
    print(f"{Colors.DIM}        Use only on authorized targets.{Colors.RESET}\n")
