#!/usr/bin/env python3
"""
Convertitore audio da MP4 a MP3 ottimizzato per videolezioni universitarie.
- Canale: Mono (-ac 1)
- Bitrate: 64 kbps (-b:a 64k)
- Di default genera un unico file MP3 completo.
- Se specificato il flag --split e la lezione supera 1 ora (3600s),
  viene divisa in 2 metà (es. lezione_part1.mp3 e lezione_part2.mp3).
- Esecuzione: container Docker con FFmpeg e Python 3
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def format_size(bytes_size: int) -> str:
    """Formatta i byte in unità leggibile (KB, MB, GB)."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def format_duration(seconds: float) -> str:
    """Formatta i secondi in stringa leggibile HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def format_timestamp(seconds: float) -> str:
    """Formatta i secondi nel formato timestamp HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def parse_time_duration(val: str | float | int) -> float:
    """
    Interpreta un valore di durata temporale.
    Supporta:
      - float o int in secondi (es. 1800, 3600.0)
      - stringa di secondi ("1800", "90s")
      - formato minuti ("30m", "45min")
      - formato ore ("1h", "1.5h")
      - formato timestamp "MM:SS" (es. "30:00") o "HH:MM:SS" (es. "01:00:00")
    """
    if isinstance(val, (int, float)):
        return float(val)

    val_str = str(val).strip()
    if not val_str:
        return 0.0

    # Formato HH:MM:SS o MM:SS
    if ":" in val_str:
        parts = val_str.split(":")
        if len(parts) == 2:
            m, s = parts
            return float(m) * 60 + float(s)
        elif len(parts) == 3:
            h, m, s = parts
            return float(h) * 3600 + float(m) * 60 + float(s)

    # Formato con unità (es. 30m, 1h, 90s, 45min)
    m_unit = re.match(r"^([\d.]+)\s*(s|sec|m|min|h|hr|ore)?$", val_str, re.IGNORECASE)
    if m_unit:
        num = float(m_unit.group(1))
        unit = (m_unit.group(2) or "s").lower()
        if unit in ["s", "sec"]:
            return num
        elif unit in ["m", "min"]:
            return num * 60.0
        elif unit in ["h", "hr", "ore"]:
            return num * 3600.0

    return float(val_str)


def find_binary(name: str) -> str | None:
    """Cerca un eseguibile nel PATH o nei percorsi di installazione tipici."""
    found = shutil.which(name)
    if found:
        return found

    common_paths = [
        f"/usr/bin/{name}",
        f"/usr/local/bin/{name}",
        rf"C:\Program Files\ffmpeg\bin\{name}.exe",
        rf"C:\ffmpeg\bin\{name}.exe",
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p
    return None


def get_media_duration(input_path: Path) -> float:
    """Rileva la durata del file video in secondi usando ffprobe o ffmpeg."""
    ffprobe_bin = find_binary("ffprobe")
    if ffprobe_bin:
        cmd = [
            ffprobe_bin,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(input_path),
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            try:
                return float(res.stdout.strip())
            except ValueError:
                pass

    # Fallback con ffmpeg analizzando lo stream info
    ffmpeg_bin = find_binary("ffmpeg")
    if ffmpeg_bin:
        cmd = [ffmpeg_bin, "-i", str(input_path)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", line)
                if m:
                    h, m_val, s = m.groups()
                    return int(h) * 3600 + int(m_val) * 60 + float(s)

    return 0.0


def convert_chunk(
    ffmpeg_bin: str,
    input_path: Path,
    output_path: Path,
    bitrate: str,
    channels: int,
    start_time: float | None = None,
    duration: float | None = None,
) -> None:
    """Esegue la conversione di un singolo segmento audio con FFmpeg."""
    cmd = [ffmpeg_bin, "-y"]
    if start_time is not None and start_time > 0:
        cmd.extend(["-ss", str(start_time)])
    cmd.extend(["-i", str(input_path)])
    if duration is not None:
        cmd.extend(["-t", str(duration)])

    cmd.extend([
        "-vn",
        "-ac", str(channels),
        "-b:a", bitrate,
        "-map_metadata", "0",
        str(output_path),
    ])

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print("\n[ERRORE] FFmpeg ha riscontrato un problema:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)


def convert_mp4_to_mp3(
    input_path: Path,
    output_path: Path | None = None,
    bitrate: str = "64k",
    channels: int = 1,
    split_threshold: float = 3600.0,
    split: bool = False,
    segment_duration: float | str | None = None,
) -> list[Path]:
    """
    Converte un file MP4 in MP3 mono a 64 kbps.
    - Se segment_duration e' specificato (> 0), divide il video in segmenti
      di durata fissa (es. ogni 1800s / 30m / 00:30:00).
    - Se split=True e duration > split_threshold (default 3600s = 1 ora),
      divide l'output in due meta': <name>_part1.mp3 e <name>_part2.mp3.
    - Altrimenti genera un unico file audio completo.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"File di input non trovato: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Il percorso specificato non è un file valido: {input_path}")
    if input_path.stat().st_size == 0:
        raise ValueError(f"Il file di input è vuoto: {input_path}")

    ffmpeg_bin = find_binary("ffmpeg")
    if not ffmpeg_bin:
        raise FileNotFoundError(
            "FFmpeg non trovato. Assicurati che FFmpeg sia disponibile nel container Docker."
        )

    # Percorso base di output
    if output_path is None:
        base_output = input_path.with_suffix(".mp3")
    else:
        base_output = Path(output_path)
    base_output.parent.mkdir(parents=True, exist_ok=True)

    initial_size = input_path.stat().st_size
    duration = get_media_duration(input_path)

    seg_sec: float | None = None
    if segment_duration is not None:
        parsed_sec = parse_time_duration(segment_duration)
        if parsed_sec > 0:
            seg_sec = parsed_sec

    # Verifica modalita' di frazionamento
    use_segments = seg_sec is not None and duration > seg_sec
    should_split = (not use_segments) and split and (duration > split_threshold)

    print("\n" + "=" * 65)
    print(" 🎙️  CONVERSIONE VIDEOLEZIONE (MP4 -> MP3 MONO 64K)")
    print("=" * 65)
    print(f"  • File sorgente:     {input_path.name}")
    print(f"  • Percorso:          {input_path.resolve()}")
    print(f"  • Dimensione video:  {format_size(initial_size)}")
    if duration > 0:
        print(f"  • Durata totale:     {format_duration(duration)} ({format_timestamp(duration)})")
    print(f"  • Formato output:    Mono (1 canale), {bitrate} MP3")

    if use_segments and seg_sec is not None:
        total_parts = int(duration // seg_sec) + (1 if (duration % seg_sec) > 0.05 else 0)
        print("-" * 65)
        print(f"  ✂️  Frazionamento per durata segmento: {format_duration(seg_sec)} ({format_timestamp(seg_sec)})")
        print(f"     - Numero stimato di parti: {total_parts}")
    elif should_split:
        half_duration = duration / 2.0
        print("-" * 65)
        print("  ✂️  Flag --split specificato e durata > 1 ora: l'audio verrà diviso in 2 metà!")
        print(f"     - Durata di ciascuna parte: {format_duration(half_duration)} ({format_timestamp(half_duration)})")
    elif split or seg_sec is not None:
        print("-" * 65)
        print("  ℹ️  La durata totale non supera la lunghezza del segmento: generato file unico.")
    print("=" * 65)

    start_clock = time.time()
    generated_files: list[Path] = []
    stem = base_output.stem
    parent = base_output.parent

    if use_segments and seg_sec is not None:
        current_start = 0.0
        part_idx = 1
        while current_start < duration:
            current_chunk_dur = min(seg_sec, duration - current_start)
            # Evita micro-spezzoni insignificanti alla fine (< 1 secondo) se non e' l'unico segmento
            if current_chunk_dur < 1.0 and part_idx > 1:
                break

            part_path = parent / f"{stem}_part{part_idx:02d}.mp3"
            end_time = min(current_start + current_chunk_dur, duration)
            print(f"\n>>> Generazione Parte {part_idx}: [{format_timestamp(current_start)} -> {format_timestamp(end_time)}] -> {part_path.name}...")
            t_chunk = time.time()
            convert_chunk(
                ffmpeg_bin=ffmpeg_bin,
                input_path=input_path,
                output_path=part_path,
                bitrate=bitrate,
                channels=channels,
                start_time=current_start,
                duration=current_chunk_dur,
            )
            print(f"    [OK] Parte {part_idx} completata in {time.time() - t_chunk:.1f}s ({format_size(part_path.stat().st_size)})")
            generated_files.append(part_path)
            current_start += current_chunk_dur
            part_idx += 1

    elif should_split:
        half_duration = duration / 2.0
        part1_path = parent / f"{stem}_part1.mp3"
        part2_path = parent / f"{stem}_part2.mp3"

        # Genera Parte 1: [0 -> half_duration]
        print(f"\n>>> Generazione Parte 1/2: [00:00:00 -> {format_timestamp(half_duration)}] -> {part1_path.name}...")
        t1 = time.time()
        convert_chunk(
            ffmpeg_bin=ffmpeg_bin,
            input_path=input_path,
            output_path=part1_path,
            bitrate=bitrate,
            channels=channels,
            start_time=0.0,
            duration=half_duration,
        )
        print(f"    [OK] Parte 1 completata in {time.time() - t1:.1f}s ({format_size(part1_path.stat().st_size)})")
        generated_files.append(part1_path)

        # Genera Parte 2: [half_duration -> fine]
        print(f"\n>>> Generazione Parte 2/2: [{format_timestamp(half_duration)} -> {format_timestamp(duration)}] -> {part2_path.name}...")
        t2 = time.time()
        convert_chunk(
            ffmpeg_bin=ffmpeg_bin,
            input_path=input_path,
            output_path=part2_path,
            bitrate=bitrate,
            channels=channels,
            start_time=half_duration,
            duration=None,
        )
        print(f"    [OK] Parte 2 completata in {time.time() - t2:.1f}s ({format_size(part2_path.stat().st_size)})")
        generated_files.append(part2_path)

    else:
        # File unico
        print(f"\n>>> Elaborazione audio in corso su file unico: {base_output.name}...")
        convert_chunk(
            ffmpeg_bin=ffmpeg_bin,
            input_path=input_path,
            output_path=base_output,
            bitrate=bitrate,
            channels=channels,
        )
        generated_files.append(base_output)

    total_time = time.time() - start_clock
    total_output_size = sum(f.stat().st_size for f in generated_files)
    saved_size = initial_size - total_output_size
    ratio = (saved_size / initial_size) * 100 if initial_size > 0 else 0

    print("\n" + "=" * 65)
    print(" [OK] Conversione ultimata con successo!")
    print(f"  • File generati ({len(generated_files)}):")
    for idx, f in enumerate(generated_files, start=1):
        print(f"     [{idx}] {f.resolve()} ({format_size(f.stat().st_size)})")
    print(f"  • Dimensione totale MP3:   {format_size(total_output_size)}")
    print(f"  • Spazio video risparmiato: {format_size(saved_size)} ({ratio:.1f}% più leggero)")
    print(f"  • Tempo totale impiegato:   {total_time:.1f} secondi")
    print("=" * 65 + "\n")

    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description="Converte videolezioni MP4 in MP3 mono compresso (64k). Di default genera un file unico; se specificato --split e supera 1h viene diviso in 2 metà."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Percorso del file video .mp4 da convertire",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Percorso base del file audio .mp3 di output (default: stesso nome e cartella dell'input)",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        type=str,
        default="64k",
        help="Bitrate audio (default: 64k)",
    )
    parser.add_argument(
        "-c",
        "--channels",
        type=int,
        default=1,
        help="Numero di canali audio (default: 1 per mono)",
    )
    parser.add_argument(
        "-s",
        "--segment",
        type=str,
        default=None,
        help="Lunghezza temporale di ciascun segmento in cui frazionare l'audio (es: '1800', '30m', '00:30:00', '1h'). Se non specificato, genera un file unico.",
    )
    parser.add_argument(
        "--split-threshold",
        type=float,
        default=3600.0,
        help="Soglia in secondi oltre la quale dividere in due metà (default: 3600s = 1 ora, usata con --split)",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Abilita la divisione dell'audio in due metà se la durata supera 1 ora (mantenuto per retrocompatibilità)",
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output) if args.output else None

    try:
        convert_mp4_to_mp3(
            input_path=input_file,
            output_path=output_file,
            bitrate=args.bitrate,
            channels=args.channels,
            split_threshold=args.split_threshold,
            split=args.split,
            segment_duration=args.segment,
        )
    except Exception as exc:
        print(f"\n[ERRORE]: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
