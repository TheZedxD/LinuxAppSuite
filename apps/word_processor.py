"""Word processor scaffold."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import Dict

from app_suite.base_app import BaseApp


class WordProcessorApp(BaseApp):
    """A lightweight word processor foundation."""

    DEFAULT_SETTINGS = {"theme": "dark", "window_size": (1100, 800)}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "Word Processor", settings_defaults=defaults)
        self.current_file: Path | None = None

    def build_ui(self, container: ttk.Frame) -> None:
        toolbar = ttk.Frame(container)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(toolbar, text="New", command=self.new_document).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Open…", command=self.open_document).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save", command=self.save_document).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save As…", command=self.save_document_as).pack(side=tk.LEFT)

        self.text_area = tk.Text(container, wrap=tk.WORD, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    # Document operations -------------------------------------------------
    def new_document(self) -> None:
        if self._confirm_discard_changes():
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            self.title(f"Word Processor - Linux App Suite")

    def open_document(self) -> None:
        if not self._confirm_discard_changes():
            return
        path = filedialog.askopenfilename(
            title="Open Document",
            initialdir=self.working_dir,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not path:
            return
        file_path = Path(path)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, file_path.read_text(encoding="utf-8"))
        self.current_file = file_path
        self.title(f"Word Processor - {file_path.name}")

    def save_document(self) -> None:
        if self.current_file is None:
            self.save_document_as()
            return
        self.current_file.write_text(self.text_area.get("1.0", tk.END), encoding="utf-8")
        messagebox.showinfo("Saved", f"Document saved to {self.current_file}")

    def save_document_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save Document As",
            defaultextension=".txt",
            initialdir=self.working_dir,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not path:
            return
        self.current_file = Path(path)
        self.save_document()

    def _confirm_discard_changes(self) -> bool:
        return messagebox.askyesno(
            "Confirm",
            "Any unsaved changes will be lost. Continue?",
            icon=messagebox.WARNING,
        )
