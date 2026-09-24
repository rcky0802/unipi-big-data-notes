"""Data Mining Playground - Environment & Dependencies Checker.

This script verifies that the Python version and essential data science
libraries (NumPy, Pandas, SciPy, Scikit-learn, Matplotlib, Seaborn)
are properly installed and ready to run the playground scripts.
"""

from __future__ import annotations

import sys
from importlib import import_module
from typing import Dict, Tuple

REQUIRED_PACKAGES: Dict[str, str] = {
    "numpy": "NumPy (linear algebra & array structures)",
    "pandas": "Pandas (data manipulation & analysis)",
    "scipy": "SciPy (scientific & statistical computing)",
    "sklearn": "Scikit-learn (machine learning & preprocessing)",
    "matplotlib": "Matplotlib (visualization engine)",
    "seaborn": "Seaborn (statistical data visualization)",
    "plotly": "Plotly (interactive graphics & web dashboard)",
}


def check_python_version() -> bool:
    """Verify minimum Python version requirement."""
    print("=" * 60)
    print("  DATA MINING PLAYGROUND - ENVIRONMENT CHECK")
    print("=" * 60)
    print(f"[*] Python Executable : {sys.executable}")
    print(f"[*] Python Version    : {sys.version.split()[0]}")

    if sys.version_info < (3, 9):
        print("[-] WARNING: Python >= 3.9 is recommended.")
        return False
    print("[+] Python version is compatible (>= 3.9).\n")
    return True


def check_libraries() -> Tuple[int, int]:
    """Test import of required libraries and print their versions."""
    print("[*] Checking required scientific packages:")
    installed = 0
    missing = 0

    for pkg_name, description in REQUIRED_PACKAGES.items():
        try:
            mod = import_module(pkg_name)
            ver = getattr(mod, "__version__", "unknown")
            print(f"  [OK] {pkg_name:<12} (v{ver:<10}) - {description}")
            installed += 1
        except ImportError:
            print(f"  [MISSING] {pkg_name:<8} - {description}")
            missing += 1

    return installed, missing


def main() -> int:
    check_python_version()
    installed, missing = check_libraries()

    print("\n" + "-" * 60)
    if missing == 0:
        print("[+] SUCCESS: All required libraries are installed!")
        print("[+] You are ready to run all scripts in the playground.")
        print("-" * 60)
        return 0
    else:
        print(f"[-] WARNING: {missing} package(s) missing out of {installed + missing}.")
        print("[-] To set up a virtual environment and install dependencies:")
        print("\n    PowerShell (Windows):")
        print("      cd Data-Mining/playground")
        print("      python -m venv .venv")
        print("      .\\.venv\\Scripts\\Activate.ps1")
        print("      pip install -r requirements.txt")
        print("\n    Bash (Linux / macOS):")
        print("      cd Data-Mining/playground")
        print("      python3 -m venv .venv")
        print("      source .venv/bin/activate")
        print("      pip install -r requirements.txt")
        print("-" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
