"""YouTube downloader scaffold."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Dict

from app_suite.base_app import BaseApp


class YouTubeDownloaderApp(BaseApp):
    """Provide a framework for future YouTube download functionality."""

    DEFAULT_SETTINGS = {"theme": "dark"}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "YouTube Downloader", settings_defaults=defaults)

    def build_ui(self, container: ttk.Frame) -> None:
        container.columnconfigure(1, weight=1)

        ttk.Label(container, text="Video URL").grid(row=0, column=0, sticky=tk.W)
        self.url_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.url_var).grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))

        ttk.Label(container, text="Save Directory").grid(row=1, column=0, sticky=tk.W, pady=(8, 0))
        self.directory_var = tk.StringVar(value=str(Path.home()))
        ttk.Entry(container, textvariable=self.directory_var).grid(row=1, column=1, sticky=tk.EW, padx=(0, 8), pady=(8, 0))

        ttk.Label(container, text="Status").grid(row=2, column=0, sticky=tk.NW, pady=(8, 0))
        self.status_box = tk.Text(container, height=10, state=tk.DISABLED)
        self.status_box.grid(row=2, column=1, sticky=tk.NSEW, pady=(8, 0))
        container.rowconfigure(2, weight=1)

        ttk.Button(container, text="Download", command=self.queue_download).grid(row=3, column=0, columnspan=2, pady=12)
        self._log_status("Ready to download. Paste a URL to begin.")

    def queue_download(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            self._log_status("Please enter a YouTube URL.")
            return
        save_dir = Path(self.directory_var.get()).expanduser()
        save_dir.mkdir(parents=True, exist_ok=True)
        self._log_status(
            "Download queuing is not yet implemented. Future versions will "
            "integrate youtube-dl or pytube for handling downloads."
        )

    def _log_status(self, message: str) -> None:
        self.status_box.configure(state=tk.NORMAL)
        self.status_box.insert(tk.END, f"{message}\n")
        self.status_box.configure(state=tk.DISABLED)
        self.status_box.see(tk.END)
