"""Pygame playground scaffold."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

from app_suite.base_app import BaseApp


class PygameHubApp(BaseApp):
    """Placeholder hub for future Pygame mini-applications."""

    DEFAULT_SETTINGS = {"theme": "dark"}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "Pygame Playground", settings_defaults=defaults)

    def build_ui(self, container: ttk.Frame) -> None:
        container.columnconfigure(0, weight=1)
        ttk.Label(
            container,
            text=(
                "This hub will host Pygame experiments.\n"
                "Use it to configure window size, frame rate, and launch demos."
            ),
            anchor=tk.CENTER,
            justify=tk.CENTER,
        ).grid(row=0, column=0, sticky=tk.NSEW, pady=40)

        ttk.Label(container, text="Desired Window Size").grid(row=1, column=0, sticky=tk.W)
        size_frame = ttk.Frame(container)
        size_frame.grid(row=2, column=0, sticky=tk.W)

        ttk.Label(size_frame, text="Width").grid(row=0, column=0, padx=(0, 8))
        self.width_var = tk.StringVar(value="800")
        ttk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=(0, 16))

        ttk.Label(size_frame, text="Height").grid(row=0, column=2, padx=(0, 8))
        self.height_var = tk.StringVar(value="600")
        ttk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=0, column=3)

        ttk.Button(container, text="Save Preferences", command=self.save_preferences).grid(row=3, column=0, pady=20)

    def save_preferences(self) -> None:
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
        except ValueError:
            self.status_var.set("Width and height must be integers.")
            return
        self.settings_manager.update(pygame_window_size=(width, height))
        self.status_var.set(f"Saved Pygame window size: {width}x{height}")
