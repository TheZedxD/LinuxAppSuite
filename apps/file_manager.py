"""File manager scaffold."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from typing import Dict

from app_suite.base_app import BaseApp


class FileManagerApp(BaseApp):
    """Basic file manager foundation with directory browsing."""

    DEFAULT_SETTINGS = {"theme": "dark"}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "File Manager", settings_defaults=defaults)

    def build_ui(self, container: ttk.Frame) -> None:
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        path_frame = ttk.Frame(container)
        path_frame.grid(row=0, column=0, sticky=tk.EW, pady=(0, 8))
        path_frame.columnconfigure(1, weight=1)

        ttk.Label(path_frame, text="Directory").grid(row=0, column=0, sticky=tk.W)
        self.path_var = tk.StringVar(value=str(self.working_dir))
        ttk.Entry(path_frame, textvariable=self.path_var).grid(row=0, column=1, sticky=tk.EW, padx=(8, 8))
        ttk.Button(path_frame, text="Browse…", command=self.choose_directory).grid(row=0, column=2)

        self.tree = ttk.Treeview(container, columns=("name", "type", "size"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size (bytes)")
        self.tree.grid(row=1, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=tk.NS)

        ttk.Button(container, text="Refresh", command=self.refresh_directory).grid(row=2, column=0, pady=8, sticky=tk.E)
        self.refresh_directory()

    def choose_directory(self) -> None:
        path = filedialog.askdirectory(initialdir=self.path_var.get() or str(self.working_dir))
        if path:
            self.path_var.set(path)
            self.refresh_directory()

    def refresh_directory(self) -> None:
        path = Path(self.path_var.get()).expanduser()
        if not path.exists():
            self.status_var.set(f"Directory not found: {path}")
            return
        self.status_var.set(f"Listing {path}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            self.status_var.set(f"Permission denied: {path}")
            return
        for entry in entries:
            entry_type = "File" if entry.is_file() else "Directory"
            size = entry.stat().st_size if entry.is_file() else "—"
            self.tree.insert("", tk.END, values=(entry.name, entry_type, size))
