#!/usr/bin/env python3
"""
organizer.py
Organizza file spostandoli per tipo o per data.
Librerie stdlib: pathlib, shutil, argparse, json, datetime
"""

from pathlib import Path
import shutil
import argparse
import json
import os
from datetime import datetime

# Regole di default: categoria -> estensioni
DEFAULT_RULES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
    "spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "code": [".py", ".js", ".java", ".c", ".cpp", ".go", ".rs", ".ts"],
}

def load_rules_from_json(path: str):
    """Carica regole da JSON. Se fallisce ritorna DEFAULT_RULES."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        normalized = {}
        for cat, exts in data.items():
            normalized[cat] = [e.lower() if e.startswith(".") else f".{e.lower()}" for e in exts]
        return normalized
    except Exception as e:
        print(f"[WARN] Errore caricando config {path}: {e}. Uso regole di default.")
        return DEFAULT_RULES

def find_category_by_extension(ext: str, rules: dict):
    ext = ext.lower()
    for cat, exts in rules.items():
        if ext in exts:
            return cat
    return None

def safe_move(src: Path, dest_dir: Path, dry_run: bool = False):
    """
    Sposta src in dest_dir. In caso di collisione aggiunge suffisso _1, _2...
    Se dry_run True -> non modifica filesystem, stampa azione prevista.
    Ritorna il Path di destinazione effettivo (o None se dry_run=True).
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        i = 1
        while True:
            candidate = dest_dir / f"{stem}_{i}{suffix}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1
    if dry_run:
        print(f"[DRY-RUN] {src} -> {dest}")
        return None
    else:
        shutil.move(str(src), str(dest))
        print(f"[OK] {src.name} -> {dest}")
        return dest

def organize_by_type(source: Path, target: Path, rules=None, dry_run=False, ignore_hidden=True):
    rules = rules or DEFAULT_RULES
    for p in source.iterdir():
        if p.is_dir():
            continue
        if ignore_hidden and p.name.startswith("."):
            continue
        cat = find_category_by_extension(p.suffix, rules)
        if cat:
            dest_dir = target / cat
        else:
            dest_dir = target / "others"
        safe_move(p, dest_dir, dry_run=dry_run)

def organize_by_date(source: Path, target: Path, date_attr="mtime", fmt="%Y/%m", dry_run=False, ignore_hidden=True):
    for p in source.iterdir():
        if p.is_dir():
            continue
        if ignore_hidden and p.name.startswith("."):
            continue
        if date_attr == "mtime":
            ts = p.stat().st_mtime
        elif date_attr == "ctime":
            ts = p.stat().st_ctime
        else:
            ts = p.stat().st_mtime
        dt = datetime.fromtimestamp(ts)
        subpath = dt.strftime(fmt)
        dest_dir = target / subpath
        safe_move(p, dest_dir, dry_run=dry_run)

def parse_args():
    ap = argparse.ArgumentParser(description="File Organizer - sposta file per tipo o per data")
    ap.add_argument("source", nargs="?", default=".", help="Cartella sorgente (default: corrente)")
    ap.add_argument("-t", "--target", default=None, help="Cartella target (default: source/organized)")
    ap.add_argument("-m", "--mode", choices=["type", "date"], default="type", help="Modalità: type o date")
    ap.add_argument("--date-attr", choices=["mtime", "ctime"], default="mtime", help="Attributo data per mode=date")
    ap.add_argument("--date-fmt", default="%Y/%m", help="Formato cartelle per date (es: %%Y/%%m)")
    ap.add_argument("-c", "--config", help="File JSON con regole per type (category->extensions)")
    ap.add_argument("--dry-run", action="store_true", help="Mostra cosa verrebbe fatto senza spostare")
    ap.add_argument("--no-ignore-hidden", dest="ignore_hidden", action="store_false", help="Non ignorare file nascosti")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    return ap.parse_args()

def main():
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    if args.target:
        target = Path(args.target).expanduser().resolve()
    else:
        target = source / "organized"
    if not source.exists() or not source.is_dir():
        print(f"Errore: source {source} non esiste o non è una cartella.")
        return
    rules = None
    if args.config:
        rules = load_rules_from_json(args.config)
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Modalità: {args.mode} {'(dry-run)' if args.dry_run else ''}")
    if args.mode == "type":
        organize_by_type(source, target, rules=rules, dry_run=args.dry_run, ignore_hidden=args.ignore_hidden)
    else:
        organize_by_date(source, target, date_attr=args.date_attr, fmt=args.date_fmt, dry_run=args.dry_run, ignore_hidden=args.ignore_hidden)
    print("Fine.")

if __name__ == "__main__":
    main()
