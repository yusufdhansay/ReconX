"""Simple colored logger for ReconX."""


class Colors:
    """ANSI color codes."""

    RESET = "\033[0m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


def info(message):
    """Print an informational message."""
    print(f"{Colors.BLUE}[*]{Colors.RESET} {message}")


def success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")


def warn(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")


def error(message):
    """Print an error message."""
    print(f"{Colors.RED}[-]{Colors.RESET} {message}")
