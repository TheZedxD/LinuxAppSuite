"""Budget planning scaffold."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import Dict, List

from app_suite.base_app import BaseApp


@dataclass
class BudgetEntry:
    category: str
    amount: float
    entry_type: str  # "income" or "expense"


class BudgetApp(BaseApp):
    """A simple budget planning interface for future expansion."""

    DEFAULT_SETTINGS = {"theme": "dark"}

    def __init__(self, master: tk.Tk, settings_defaults: Dict[str, object] | None = None) -> None:
        defaults = dict(self.DEFAULT_SETTINGS)
        if settings_defaults:
            defaults.update(settings_defaults)
        super().__init__(master, "Budget Planner", settings_defaults=defaults)
        self.entries: List[BudgetEntry] = []

    def build_ui(self, container: ttk.Frame) -> None:
        container.columnconfigure(0, weight=1)

        form = ttk.Frame(container)
        form.pack(fill=tk.X, pady=(0, 12))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Category").grid(row=0, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.category_var).grid(row=0, column=1, sticky=tk.EW, padx=(8, 8))

        ttk.Label(form, text="Amount").grid(row=1, column=0, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var).grid(row=1, column=1, sticky=tk.EW, padx=(8, 8))

        ttk.Label(form, text="Type").grid(row=2, column=0, sticky=tk.W)
        self.type_var = tk.StringVar(value="income")
        type_selector = ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["income", "expense"],
            state="readonly",
        )
        type_selector.grid(row=2, column=1, sticky=tk.EW, padx=(8, 8))
        type_selector.current(0)

        ttk.Button(form, text="Add Entry", command=self.add_entry).grid(row=3, column=0, columnspan=2, pady=8)

        columns = ("category", "type", "amount")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
        self.tree.column("amount", anchor=tk.E, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.summary_var = tk.StringVar(value="Total Income: 0.00 | Total Expense: 0.00 | Balance: 0.00")
        ttk.Label(container, textvariable=self.summary_var, anchor=tk.E).pack(fill=tk.X, pady=(8, 0))

    def add_entry(self) -> None:
        category = self.category_var.get().strip()
        amount_text = self.amount_var.get().strip()
        entry_type = self.type_var.get()
        if not category or not amount_text:
            return
        try:
            amount = float(amount_text)
        except ValueError:
            return
        entry = BudgetEntry(category=category, amount=amount, entry_type=entry_type)
        self.entries.append(entry)
        self.tree.insert("", tk.END, values=(entry.category, entry.entry_type.title(), f"{entry.amount:.2f}"))
        self._update_summary()
        self.category_var.set("")
        self.amount_var.set("")

    def _update_summary(self) -> None:
        total_income = sum(entry.amount for entry in self.entries if entry.entry_type == "income")
        total_expense = sum(entry.amount for entry in self.entries if entry.entry_type == "expense")
        balance = total_income - total_expense
        self.summary_var.set(
            f"Total Income: {total_income:.2f} | Total Expense: {total_expense:.2f} | Balance: {balance:.2f}"
        )
