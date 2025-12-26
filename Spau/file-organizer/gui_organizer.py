#!/usr/bin/env python3
"""
Interfaccia GUI minima per organizer (tkinter).
Usa le funzioni di organizer.py. Drag&drop opzionale con tkinterdnd2 se installato.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

try:
    from organizer import organize_by_type, organize_by_date, load_rules_from_json
except Exception:
    raise RuntimeError("Assicurati che organizer.py sia nello stesso folder e importabile.")

USE_TKDND = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    USE_TKDND = True
except Exception:
    USE_TKDND = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("File Organizer - GUI")
        self.source = Path(".").resolve()
        self.target = self.source / "organized"
        self.config_path = None

        frm = ttk.Frame(root, padding=10)
        frm.grid(sticky="nsew")

        ttk.Label(frm, text="Sorgente:").grid(column=0, row=0, sticky="w")
        self.src_var = tk.StringVar(value=str(self.source))
        ttk.Entry(frm, textvariable=self.src_var, width=50).grid(column=1, row=0, sticky="we")
        ttk.Button(frm, text="Scegli...", command=self.choose_source).grid(column=2, row=0)

        ttk.Label(frm, text="Target:").grid(column=0, row=1, sticky="w")
        self.tgt_var = tk.StringVar(value=str(self.target))
        ttk.Entry(frm, textvariable=self.tgt_var, width=50).grid(column=1, row=1, sticky="we")
        ttk.Button(frm, text="Scegli...", command=self.choose_target).grid(column=2, row=1)

        ttk.Label(frm, text="Modalità:").grid(column=0, row=2, sticky="w")
        self.mode_var = tk.StringVar(value="type")
        ttk.Radiobutton(frm, text="Per tipo", variable=self.mode_var, value="type").grid(column=1, row=2, sticky="w")
        ttk.Radiobutton(frm, text="Per data", variable=self.mode_var, value="date").grid(column=1, row=2, sticky="e")

        ttk.Button(frm, text="Scegli config JSON (opzionale)", command=self.choose_config).grid(column=0, row=3, columnspan=3, sticky="we", pady=(6,0))
        ttk.Button(frm, text="Avvia organizzazione", command=self.start_organize).grid(column=0, row=4, columnspan=3, sticky="we", pady=(8,0))
        self.status = tk.StringVar(value="Pronto")
        ttk.Label(frm, textvariable=self.status).grid(column=0, row=5, columnspan=3, sticky="w", pady=(6,0))

    def choose_source(self):
        p = filedialog.askdirectory(initialdir=str(self.source))
        if p:
            self.src_var.set(p)

    def choose_target(self):
        p = filedialog.askdirectory(initialdir=str(self.target))
        if p:
            self.tgt_var.set(p)

    def choose_config(self):
        p = filedialog.askopenfilename(filetypes=[("JSON files","*.json"),("All files","*.*")])
        if p:
            self.config_path = p
            self.status.set(f"Config: {p}")

    def start_organize(self):
        src = Path(self.src_var.get())
        tgt = Path(self.tgt_var.get())
        if not src.exists():
            messagebox.showerror("Errore", f"Sorgente non esiste: {src}")
            return
        t = threading.Thread(target=self.run_organize, args=(src, tgt, self.mode_var.get(), self.config_path), daemon=True)
        t.start()

    def run_organize(self, src, tgt, mode, config_path):
        self.status.set("Organizzazione in corso...")
        try:
            rules = None
            if config_path:
                rules = load_rules_from_json(config_path)
            if mode == "type":
                organize_by_type(src, tgt, rules=rules, dry_run=False)
            else:
                organize_by_date(src, tgt, date_attr="mtime", fmt="%Y/%m", dry_run=False)
            self.status.set("Completato.")
            messagebox.showinfo("Fine", "Organizzazione completata.")
        except Exception as e:
            self.status.set("Errore")
            messagebox.showerror("Errore", str(e))

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
