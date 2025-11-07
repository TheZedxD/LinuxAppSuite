"""Base classes for Linux App Suite Tkinter applications."""
from __future__ import annotations

import tkinter as tk
from tkinter import Menu, ttk
from pathlib import Path
from typing import Dict, Optional

from .settings_manager import SettingsManager
from .theme import Theme, apply_theme, available_themes, get_theme


class BaseApp(tk.Toplevel):
    """Shared window behaviour for suite applications."""

    DEFAULT_SIZE = (1024, 768)
    MIN_SIZE = (640, 480)

    def __init__(
        self,
        master: tk.Tk,
        app_name: str,
        settings_defaults: Optional[Dict[str, object]] = None,
    ) -> None:
        super().__init__(master=master)
        self.app_name = app_name
        self.working_dir = Path.cwd()
        defaults = {"theme": "dark", "window_size": self.DEFAULT_SIZE}
        if settings_defaults:
            defaults.update(settings_defaults)
        self.settings_manager = SettingsManager(app_name, defaults=defaults)
        self._theme_name = self.settings_manager.get("theme", "dark")
        window_size = tuple(self.settings_manager.get("window_size", self.DEFAULT_SIZE))

        self.title(f"{self.app_name} - Linux App Suite")
        self.geometry(f"{int(window_size[0])}x{int(window_size[1])}")
        self.minsize(*self.MIN_SIZE)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._create_menu_bar()

        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.status_var = tk.StringVar(value=f"Working directory: {self.working_dir}")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=(0, 8))

        self.build_ui(self.container)
        self.apply_theme(self._theme_name)

    # region UI scaffolding -------------------------------------------------
    def _create_menu_bar(self) -> None:
        menu_bar = Menu(self)
        settings_menu = Menu(menu_bar, tearoff=False)
        theme_menu = Menu(settings_menu, tearoff=False)
        for theme_name in available_themes():
            theme_menu.add_command(
                label=theme_name.title(),
                command=lambda name=theme_name: self.apply_theme(name, persist=True),
            )
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        settings_menu.add_command(label="Reset Window Size", command=self.reset_window_size)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        self.config(menu=menu_bar)

    # endregion -------------------------------------------------------------

    def build_ui(self, container: ttk.Frame) -> None:  # pragma: no cover - to be overridden
        """Hook for subclasses to populate the main content area."""

    def apply_theme(self, theme_name: str, persist: bool = False) -> None:
        """Apply the selected theme and optionally persist it."""

        theme: Theme = get_theme(theme_name)
        apply_theme(self, theme)
        self._theme_name = theme.name
        if persist:
            self.settings_manager.update(theme=theme.name)

    def reset_window_size(self) -> None:
        """Restore the default window size and persist it."""

        self.geometry(f"{self.DEFAULT_SIZE[0]}x{self.DEFAULT_SIZE[1]}")
        self.settings_manager.update(window_size=self.DEFAULT_SIZE)

    def on_close(self) -> None:
        """Persist window geometry on close."""

        self.settings_manager.update(window_size=(self.winfo_width(), self.winfo_height()))
        self.destroy()
