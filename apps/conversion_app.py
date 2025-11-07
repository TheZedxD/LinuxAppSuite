"""Conversion utility framework."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict

from app_suite.base_app import BaseApp


class ConversionApp(BaseApp):
    """A starter conversion utility with common unit conversions."""

    DEFAULT_SETTINGS = {"theme": "dark"}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "Conversion Utility", settings_defaults=defaults)

    def build_ui(self, container: ttk.Frame) -> None:
        container.columnconfigure(1, weight=1)

        ttk.Label(container, text="Conversion Type").grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        self.conversion_var = tk.StringVar()

        self.conversions: Dict[str, Callable[[float], float]] = {
            "Inches → Centimeters": lambda value: value * 2.54,
            "Centimeters → Inches": lambda value: value / 2.54,
            "Fahrenheit → Celsius": lambda value: (value - 32) * 5 / 9,
            "Celsius → Fahrenheit": lambda value: (value * 9 / 5) + 32,
        }

        self.conversion_selector = ttk.Combobox(
            container,
            textvariable=self.conversion_var,
            values=list(self.conversions.keys()),
            state="readonly",
        )
        self.conversion_selector.grid(row=0, column=1, sticky=tk.EW, pady=(0, 8))
        self.conversion_selector.current(0)

        ttk.Label(container, text="Input Value").grid(row=1, column=0, sticky=tk.W)
        self.input_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.input_var).grid(row=1, column=1, sticky=tk.EW)

        ttk.Button(container, text="Convert", command=self.perform_conversion).grid(
            row=2, column=0, columnspan=2, pady=12
        )

        ttk.Label(container, text="Result").grid(row=3, column=0, sticky=tk.W)
        self.output_var = tk.StringVar(value="Ready")
        ttk.Label(container, textvariable=self.output_var).grid(row=3, column=1, sticky=tk.W)

    def perform_conversion(self) -> None:
        selection = self.conversion_var.get()
        raw_value = self.input_var.get().strip()
        if not raw_value:
            self.output_var.set("Enter a value to convert.")
            return
        try:
            value = float(raw_value)
            converter = self.conversions.get(selection)
            if not converter:
                self.output_var.set("Unknown conversion type.")
                return
            result = converter(value)
            self.output_var.set(f"{result:.2f}")
        except ValueError:
            self.output_var.set("Input must be numeric.")
