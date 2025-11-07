"""Entry point for the Linux App Suite."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, Menu

from app_suite.app_registry import registered_apps
from app_suite.settings_manager import SettingsManager
from app_suite.theme import apply_theme, available_themes, get_theme


class AppSuiteLauncher(tk.Tk):
    """Main window listing available applications."""

    DEFAULT_SIZE = (1024, 768)

    def __init__(self) -> None:
        super().__init__()
        self.title("Linux App Suite")
        self.settings_manager = SettingsManager(
            "Launcher",
            defaults={"theme": "dark", "window_size": self.DEFAULT_SIZE},
        )
        window_size = tuple(self.settings_manager.get("window_size", self.DEFAULT_SIZE))
        self.geometry(f"{int(window_size[0])}x{int(window_size[1])}")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.minsize(640, 480)

        self._theme_name = self.settings_manager.get("theme", "dark")
        self._create_menu_bar()

        self.header = ttk.Label(self, text="Welcome to the Linux App Suite", font=("Segoe UI", 18, "bold"))
        self.header.pack(pady=(24, 12))

        self.subtitle = ttk.Label(
            self,
            text=(
                "Choose an application to launch. Each tool maintains its own settings "
                "including theme and window layout."
            ),
            wraplength=600,
            justify=tk.CENTER,
        )
        self.subtitle.pack(pady=(0, 24))

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=16)
        self.button_frame.columnconfigure(0, weight=1)

        self._populate_app_buttons()
        self.apply_theme(self._theme_name)

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

    def _populate_app_buttons(self) -> None:
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        apps = registered_apps()
        for row, (app_name, app_class) in enumerate(apps.items()):
            button = ttk.Button(
                self.button_frame,
                text=app_name,
                command=lambda cls=app_class: self.launch_app(cls),
                width=40,
            )
            button.grid(row=row, column=0, pady=8)

    def apply_theme(self, theme_name: str, persist: bool = False) -> None:
        theme = get_theme(theme_name)
        apply_theme(self, theme)
        self._theme_name = theme.name
        if persist:
            self.settings_manager.update(theme=theme.name)

    def reset_window_size(self) -> None:
        self.geometry(f"{self.DEFAULT_SIZE[0]}x{self.DEFAULT_SIZE[1]}")
        self.settings_manager.update(window_size=self.DEFAULT_SIZE)

    def launch_app(self, app_class) -> None:
        app_class(self, settings_defaults={"theme": self._theme_name})

    def on_close(self) -> None:
        self.settings_manager.update(window_size=(self.winfo_width(), self.winfo_height()))
        self.destroy()


def main() -> None:
    launcher = AppSuiteLauncher()
    launcher.mainloop()


if __name__ == "__main__":
    main()
