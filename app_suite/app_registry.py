"""Application registry for the Linux App Suite."""
from __future__ import annotations

from typing import Dict, Type

from app_suite.base_app import BaseApp
from apps.conversion_app import ConversionApp
from apps.word_processor import WordProcessorApp
from apps.file_manager import FileManagerApp
from apps.youtube_downloader import YouTubeDownloaderApp
from apps.budget_app import BudgetApp
from apps.pygame_hub import PygameHubApp


_APP_REGISTRY: Dict[str, Type[BaseApp]] = {
    "Conversion Utility": ConversionApp,
    "Word Processor": WordProcessorApp,
    "File Manager": FileManagerApp,
    "YouTube Downloader": YouTubeDownloaderApp,
    "Budget Planner": BudgetApp,
    "Pygame Playground": PygameHubApp,
}


def registered_apps() -> Dict[str, Type[BaseApp]]:
    """Return a shallow copy of registered applications."""

    return dict(_APP_REGISTRY)
