#!/usr/bin/env python3
"""
Sistema di Smart Build unificato e cross-platform per dispense universitarie in italiano.
Supporta compilazione differenziale (solo materie modificate), fallback trasparente tra
latexmk locale e container Docker, e sincronizzazione automatica dei PDF in pdf/.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Colori ANSI per output terminale
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_GRAY = "\033[90m"


def print_colored(text: str, color: str = COLOR_RESET) -> None:
    if sys.stdout.isatty() or os.environ.get("TERM"):
        print(f"{color}{text}{COLOR_RESET}")
    else:
        print(text)


def find_subjects(root_dir: Path) -> list[Path]:
    """Trova tutte le cartelle materia che contengono un file sorgente LaTeX principale."""
    subjects = []
    for item in sorted(root_dir.iterdir()):
        if item.is_dir() and not item.name.startswith(".") and item.name not in ("pdf", "scripts"):
            if (item / "main.tex").is_file() or (item / "main_it.tex").is_file():
                subjects.append(item)
    return subjects


def check_target_modified(dir_path: Path, lang: str = "it") -> dict:
    """
    Verifica se la materia necessita di compilazione confrontando il timestamp del PDF
    con tutti i file sorgente (.tex, .bib, assets).
    """
    lang_lower = lang.lower()
    # In Opzione A, il file principale unificato è main.tex (con fallback a main_<lang>.tex se presente)
    if (dir_path / "main.tex").is_file():
        tex_file = "main.tex"
    elif (dir_path / f"main_{lang_lower}.tex").is_file():
        tex_file = f"main_{lang_lower}.tex"
    else:
        return {
            "exists": False,
            "is_modified": False,
            "reason": "File sorgente main.tex non presente",
            "tex_file": "main.tex",
            "pdf_file": None,
        }

    full_tex_path = dir_path / tex_file

    pdf_file = Path(tex_file).stem + ".pdf"
    pdf_path = dir_path / pdf_file

    if not pdf_path.is_file():
        return {
            "exists": True,
            "is_modified": True,
            "reason": f"PDF ({pdf_file}) non ancora generato",
            "tex_file": tex_file,
            "pdf_file": pdf_file,
        }

    pdf_mtime = pdf_path.stat().st_mtime

    sources: list[Path] = [full_tex_path]

    preamble = dir_path / "config" / f"preamble_{lang_lower}.tex"
    if preamble.is_file():
        sources.append(preamble)

    bib = dir_path / "references.bib"
    if bib.is_file():
        sources.append(bib)

    chap_dir = dir_path / "chapters" / lang_lower
    if chap_dir.is_dir():
        sources.extend(chap_dir.rglob("*.tex"))

    asset_dir = dir_path / "assets"
    if asset_dir.is_dir():
        for f in asset_dir.rglob("*"):
            if f.is_file():
                sources.append(f)

    for src in sources:
        try:
            mtime = src.stat().st_mtime
            if mtime > pdf_mtime:
                mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                return {
                    "exists": True,
                    "is_modified": True,
                    "reason": f"'{src.name}' modificato il {mtime_str}",
                    "tex_file": tex_file,
                    "pdf_file": pdf_file,
                }
        except OSError:
            continue

    return {
        "exists": True,
        "is_modified": False,
        "reason": "PDF aggiornato",
        "tex_file": tex_file,
        "pdf_file": pdf_file,
    }


def detect_compiler(root_dir: Path) -> tuple[str, list[str]]:
    """
    Rileva se compilare tramite latexmk nativo o container Docker.
    Ritorna una tupla (tipo_motore, comando_base).
    """
    # 1. Preferisci latexmk locale se presente
    latexmk_path = shutil.which("latexmk")
    if latexmk_path:
        return ("local", [latexmk_path])

    # 2. In alternativa, verifica Docker
    docker_path = shutil.which("docker")
    if docker_path:
        try:
            res = subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            if res.returncode == 0:
                compose_file = root_dir / "docker-compose.yml"
                return ("docker", ["docker", "compose", "-f", str(compose_file)])
        except Exception:
            pass

    return ("none", [])


def clean_artifacts(root_dir: Path, subjects: list[Path]) -> None:
    """Pulisce file e cartelle temporanee generate da LaTeX."""
    aux_extensions = {
        ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls",
        ".idx", ".ilg", ".ind", ".lof", ".log", ".out", ".run.xml",
        ".synctex.gz", ".synctex", ".toc", ".nav", ".snm", ".vrb", ".xdv"
    }

    print_colored("Pulizia artefatti ausiliari LaTeX in corso...", COLOR_CYAN)

    for subj in subjects:
        print_colored(f"--> Pulizia cartella: {subj.name}...", COLOR_GRAY)
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

    print_colored("Pulizia completata con successo.", COLOR_GREEN)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smart Build differenziale unificato per dispense LaTeX."
    )
    parser.add_argument(
        "-s", "--subject",
        nargs="+",
        help="Specifica una o più materie (anche parziale, es: Data-Mining Algorithm-Engineering)",
    )
    parser.add_argument(
        "-l", "--lang",
        default="IT",
        choices=["IT", "it"],
        help="Specifica la lingua da compilare (default: IT)",
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Forza la compilazione di tutte le materie",
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Forza la ricompilazione anche se non sono rilevate modifiche",
    )
    parser.add_argument(
        "-c", "--clean",
        action="store_true",
        help="Pulisce i file ausiliari di compilazione",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Non copiare i PDF generati nella cartella pdf/",
    )

    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    pdf_out_dir = root_dir / "pdf"

    subjects = find_subjects(root_dir)
    if not subjects:
        print_colored(f"[ERRORE] Nessuna cartella materia trovata in {root_dir}.", COLOR_RED)
        return 1

    if args.clean:
        clean_artifacts(root_dir, subjects)
        return 0

    # Filtra materie se specificate
    selected_dirs = subjects
    if args.subject:
        filtered = []
        for term in args.subject:
            matched = [s for s in subjects if term.lower() in s.name.lower()]
            filtered.extend(matched)
        selected_dirs = sorted(list(set(filtered)), key=lambda p: p.name)
        if not selected_dirs:
            available = ", ".join(s.name for s in subjects)
            print_colored(
                f"[ERRORE] Nessuna materia corrisponde a '{', '.join(args.subject)}'. "
                f"Disponibili: {available}",
                COLOR_RED,
            )
            return 1

    # Rilevamento motore di compilazione
    engine_type, engine_cmd = detect_compiler(root_dir)
    if engine_type == "none":
        print_colored("\n[ERRORE] Né 'latexmk' né 'docker' sono disponibili nel PATH.", COLOR_RED)
        print_colored("Installare TeX Live con latexmk o avviare Docker Desktop.\n", COLOR_YELLOW)
        return 1

    if engine_type == "local":
        print_colored("[INFO] Motore di compilazione: LaTeX locale (latexmk)", COLOR_GREEN)
    else:
        print_colored("[INFO] Motore di compilazione: Container Docker (latexmk)", COLOR_GREEN)

    # Analisi modifiche
    build_plan = []
    skipped_plan = []

    for subj in selected_dirs:
        check = check_target_modified(subj, args.lang)
        if check["exists"]:
            reason = "Compilazione forzata" if (args.force or args.all) else check["reason"]
            needs_build = args.force or args.all or check["is_modified"]
            item = {
                "dir": subj,
                "subject": subj.name,
                "lang": args.lang.upper(),
                "tex_file": check["tex_file"],
                "pdf_file": check["pdf_file"],
                "reason": reason,
                "needs_build": needs_build,
            }
            if needs_build:
                build_plan.append(item)
            else:
                skipped_plan.append(item)

    print_colored("\n==================================================", COLOR_CYAN)
    print_colored("         PIANO DI COMPILAZIONE DISPENSE", COLOR_CYAN)
    print_colored("==================================================", COLOR_CYAN)

    if skipped_plan:
        print_colored("\nDispense già aggiornate (SKIP):", COLOR_GRAY)
        for item in skipped_plan:
            print_colored(f"  - [{item['lang']}] {item['subject']}: {item['reason']}", COLOR_GRAY)

    if not build_plan:
        print_colored(
            f"\n[OK] Tutte le dispense ({args.lang.upper()}) sono già compilate e aggiornate!",
            COLOR_GREEN,
        )
        print_colored("     (Usa -f / --force per ricompilare comunque)\n", COLOR_GRAY)
        return 0

    print_colored(f"\nDispense da compilare ({len(build_plan)}):", COLOR_YELLOW)
    for item in build_plan:
        print_colored(
            f"  * [{item['lang']}] {item['subject']} ({item['tex_file']}) -> {item['reason']}",
            COLOR_YELLOW,
        )
    print_colored("--------------------------------------------------", COLOR_CYAN)

    if not args.no_sync and not pdf_out_dir.exists():
        pdf_out_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    fail_count = 0

    for item in build_plan:
        subj_dir: Path = item["dir"]
        subj_name = item["subject"]
        lang = item["lang"]
        tex_file = item["tex_file"]
        pdf_file = item["pdf_file"]

        print_colored(f"\n>>> [{lang}] Compilazione: {subj_name} ({tex_file})...", COLOR_CYAN)

        if engine_type == "local":
            cmd = [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-emulate-aux-dir",
                "-auxdir=build",
                tex_file,
            ]
            cwd = subj_dir
        else:
            cmd = engine_cmd + [
                "run",
                "--rm",
                "-w",
                f"/workspace/{subj_name}",
                "app",
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-emulate-aux-dir",
                "-auxdir=build",
                tex_file,
            ]
            cwd = root_dir

        try:
            res = subprocess.run(cmd, cwd=cwd)
            if res.returncode == 0:
                print_colored(f"[OK] Compilato con successo: {subj_name} [{lang}]", COLOR_GREEN)
                success_count += 1

                # Sincronizza PDF in pdf/
                if not args.no_sync and pdf_file:
                    generated_pdf = subj_dir / pdf_file
                    if generated_pdf.is_file():
                        target_pdf = pdf_out_dir / f"{subj_name}-{lang}.pdf"
                        shutil.copy2(generated_pdf, target_pdf)
                        print_colored(f"     PDF salvato in: pdf/{subj_name}-{lang}.pdf", COLOR_GRAY)
            else:
                print_colored(
                    f"[ERRORE] Fallimento compilazione per {subj_name} [{lang}] "
                    f"(exit code: {res.returncode})",
                    COLOR_RED,
                )
                fail_count += 1
        except Exception as e:
            print_colored(f"[ECCEZIONE] Errore critico per {subj_name} [{lang}]: {e}", COLOR_RED)
            fail_count += 1

    print_colored("\n==================================================", COLOR_CYAN)
    print_colored(
        f"  Riepilogo finale: {success_count} riuscite, {fail_count} fallite",
        COLOR_CYAN,
    )
    print_colored("==================================================\n", COLOR_CYAN)

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
