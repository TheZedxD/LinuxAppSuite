"""Theme definitions and helpers for the Linux App Suite."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import tkinter as tk
from tkinter import ttk


@dataclass(frozen=True)
class Theme:
    """UI color palette used across the suite."""

    name: str
    background: str
    foreground: str
    accent: str
    input_background: str
    input_foreground: str


_THEMES: Dict[str, Theme] = {
    "dark": Theme(
        name="dark",
        background="#1e1e1e",
        foreground="#f0f0f0",
        accent="#2d89ef",
        input_background="#2a2a2a",
        input_foreground="#f0f0f0",
    ),
    "light": Theme(
        name="light",
        background="#f5f5f5",
        foreground="#1a1a1a",
        accent="#0078d4",
        input_background="#ffffff",
        input_foreground="#1a1a1a",
    ),
}


def available_themes() -> Dict[str, Theme]:
    """Return a copy of registered themes."""

    return dict(_THEMES)


def get_theme(name: str) -> Theme:
    """Return a theme by name, falling back to dark."""

    return _THEMES.get(name, _THEMES["dark"])


def apply_theme(widget: tk.Widget, theme: Theme) -> None:
    """Apply the theme recursively to the widget tree."""

    if isinstance(widget, (tk.Tk, tk.Toplevel, tk.Frame)):
        widget.configure(bg=theme.background)
    elif isinstance(widget, (tk.Label, tk.Button, tk.Checkbutton, tk.Radiobutton, tk.Listbox)):
        widget.configure(bg=theme.background, fg=theme.foreground, activebackground=theme.accent)
    elif isinstance(widget, tk.Entry):
        widget.configure(
            bg=theme.input_background,
            fg=theme.input_foreground,
            insertbackground=theme.input_foreground,
        )

    style = ttk.Style(widget)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "TLabel",
        background=theme.background,
        foreground=theme.foreground,
    )
    style.configure(
        "TButton",
        background=theme.accent,
        foreground=theme.foreground,
    )
    style.map(
        "TButton",
        background=[("active", theme.accent)],
        foreground=[("active", theme.foreground)],
    )
    style.configure(
        "TFrame",
        background=theme.background,
    )
    style.configure(
        "TEntry",
        fieldbackground=theme.input_background,
        foreground=theme.input_foreground,
    )
    style.configure(
        "Treeview",
        background=theme.input_background,
        fieldbackground=theme.input_background,
        foreground=theme.input_foreground,
    )
    style.configure(
        "Treeview.Heading",
        background=theme.background,
        foreground=theme.foreground,
    )

    for child in widget.winfo_children():
        apply_theme(child, theme)
