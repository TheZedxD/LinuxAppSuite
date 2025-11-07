# Linux App Suite

The Linux App Suite is a collection of desktop utilities implemented with Tkinter. The
suite provides a unified launcher, shared theming, and per-application settings storage
so that each tool can adopt common conventions while remaining customizable.

## Features

- **Unified launcher** – start applications from a central hub with consistent window
  sizing defaults (1024×768) and quick theme switching.
- **Theme support** – light and dark themes are available globally. The chosen theme is
  persisted for the launcher and each individual app.
- **Per-app settings** – window size, theme, and other configuration values are saved in
  `~/.linux_app_suite/<app>.json` and loaded automatically.
- **Initial application scaffolds**:
  - Conversion Utility (length and temperature conversions)
  - Word Processor (basic text editing and file operations)
  - File Manager (directory browser)
  - YouTube Downloader (interface prepared for future download logic)
  - Budget Planner (track income and expenses)
  - Pygame Playground (configure defaults for future Pygame projects)

## Getting Started

1. Ensure Python 3.10+ is installed along with Tkinter.
2. Run the launcher:

   ```bash
   python main.py
   ```

3. Choose an application from the launcher window. Each app opens in its own window,
   saves its window size, and remembers the selected theme the next time it is launched.

## Project Structure

```
app_suite/            Shared infrastructure (themes, settings, base classes)
apps/                 Individual application scaffolds
main.py               Launcher entry point
README.md             Project overview
```

## Next Steps

- Flesh out application-specific functionality (e.g., integrate youtube-dl for downloads,
  implement file operations, add document formatting, etc.).
- Expand the theme system with additional palettes and component styles.
- Add automated tests around settings persistence and conversion calculations.
