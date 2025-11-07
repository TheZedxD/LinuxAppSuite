"""Application scaffolds for the Linux App Suite."""

from .conversion_app import ConversionApp
from .word_processor import WordProcessorApp
from .file_manager import FileManagerApp
from .youtube_downloader import YouTubeDownloaderApp
from .budget_app import BudgetApp
from .pygame_hub import PygameHubApp

__all__ = [
    "ConversionApp",
    "WordProcessorApp",
    "FileManagerApp",
    "YouTubeDownloaderApp",
    "BudgetApp",
    "PygameHubApp",
]
