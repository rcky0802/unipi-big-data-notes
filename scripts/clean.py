#!/usr/bin/env python3
"""
Script di pulizia artefatti ausiliari LaTeX per tutte le materie (cross-platform).
"""

import sys
import shutil
from pathlib import Path

# Colori ANSI
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_GRAY = "\033[90m"


def main() -> int:
    root_dir = Path(__file__).resolve().parent.parent

    aux_extensions = {
        ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls",
        ".idx", ".ilg", ".ind", ".lof", ".log", ".out", ".run.xml",
        ".synctex.gz", ".synctex", ".toc", ".nav", ".snm", ".vrb", ".xdv"
    }

    subjects = [
        item for item in sorted(root_dir.iterdir())
        if item.is_dir() and not item.name.startswith(".") and item.name not in ("pdf", "scripts")
        and ((item / "main_it.tex").is_file() or (item / "main.tex").is_file())
    ]

    print(f"{COLOR_CYAN}Pulizia artefatti ausiliari LaTeX in corso...{COLOR_RESET}")

    for subj in subjects:
        print(f"{COLOR_GRAY}--> Pulizia cartella: {subj.name}...{COLOR_RESET}")
        build_dir = subj / "build"
        if build_dir.is_dir():
            shutil.rmtree(build_dir, ignore_errors=True)

        for f in subj.rglob("*"):
            if f.is_file():
                if f.suffix in aux_extensions or any(f.name.endswith(ext) for ext in aux_extensions):
                    try:
                        f.unlink()
                    except OSError:
                        pass

    print(f"{COLOR_GREEN}Pulizia completata con successo.{COLOR_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
