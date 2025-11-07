"""Settings persistence for Linux App Suite applications."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsManager:
    """Load and persist per-application settings."""

    def __init__(
        self,
        app_name: str,
        defaults: Optional[Dict[str, Any]] = None,
        config_dir: Optional[Path] = None,
    ) -> None:
        self.app_name = app_name
        self.defaults = defaults or {}
        self.config_dir = config_dir or Path.home() / ".linux_app_suite"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(ch if ch.isalnum() else "_" for ch in app_name.lower())
        self.file_path = self.config_dir / f"{safe_name}.json"
        self._settings: Dict[str, Any] = {}
        self.load()

    @property
    def settings(self) -> Dict[str, Any]:
        """Return the current settings."""

        return dict(self._settings)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a setting value, checking defaults if needed."""

        if key in self._settings:
            return self._settings[key]
        return self.defaults.get(key, default)

    def update(self, **values: Any) -> None:
        """Update stored values and persist them to disk."""

        self._settings.update(values)
        self.save()

    def load(self) -> None:
        """Load settings from disk, merging with defaults."""

        settings = dict(self.defaults)
        if self.file_path.exists():
            try:
                data = json.loads(self.file_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    settings.update(data)
            except json.JSONDecodeError:
                # Corrupted settings will be overwritten with defaults.
                pass
        self._settings = settings

    def save(self) -> None:
        """Persist settings to disk."""

        serialized = self._settings.copy()
        # Ensure tuples are stored as lists for JSON compatibility.
        for key, value in list(serialized.items()):
            if isinstance(value, tuple):
                serialized[key] = list(value)
        self.file_path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")
