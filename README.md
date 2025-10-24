# LinuxAppSuite

A personal collection of Python, web apps, and utilities designed for easy setup on any Linux machine. All applications created and maintained by Dovendyr.

## Features

- Automatic OS detection and dependency installation
- Cross-distribution support (Ubuntu, Debian, Fedora, CentOS, Arch, openSUSE)
- Easy setup scripts for each application

## Applications

### 1. Ollama Chat - Local AI Chat Application

A robust Tkinter-based chat interface for Ollama with advanced features:

**Features:**
- Real-time streaming text responses
- Model selection from locally available Ollama models
- Tool calling support (cryptocurrency data via CoinGecko API)
- Syntax-highlighted code blocks with colored backgrounds
- Persistent chat history with save/load functionality
- Clean, intuitive UI
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

**Quick Start:**
```bash
# Run the installation script
cd LinuxAppSuite
bash scripts/install/setup_ollama_chat.sh

# Start the application
cd python-apps/ollama-chat
python3 ollama_chat.py
```

**Prerequisites:**
- Python 3.6+
- Tkinter
- Ollama installed and running

**Tools Available:**
- `get_top_cryptocurrencies` - Fetch top 10 cryptocurrencies by market cap with live prices

## Installation

### General Setup

Clone the repository:
```bash
git clone https://github.com/TheZedxD/LinuxAppSuite.git
cd LinuxAppSuite
```

Each application has its own setup script in `scripts/install/`.

### Manual Dependency Installation

The suite automatically detects your Linux distribution and uses the appropriate package manager. Supported distributions:

- **Debian/Ubuntu**: apt
- **Fedora**: dnf
- **CentOS/RHEL**: yum
- **Arch Linux**: pacman
- **openSUSE**: zypper

## Project Structure

```
LinuxAppSuite/
├── python-apps/          # Python applications
│   └── ollama-chat/      # Ollama chat application
│       ├── ollama_chat.py    # Main application
│       ├── ollama_client.py  # Ollama API client
│       └── tools.py          # Tool definitions
├── scripts/              # Setup and utility scripts
│   └── install/          # Installation scripts
│       └── setup_ollama_chat.sh
├── utils/                # Shared utilities
│   └── os_detect.py      # OS detection utility
└── README.md
```

## Usage

### Ollama Chat Application

1. Make sure Ollama is installed and running:
   ```bash
   ollama serve
   ```

2. Pull a model (if you haven't already):
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```

3. Run the chat application:
   ```bash
   cd python-apps/ollama-chat
   python3 ollama_chat.py
   ```

4. Select a model from the dropdown and start chatting!

5. Try asking: "What are the top 10 cryptocurrencies?" to test the tool calling feature.

## Adding More Applications

This suite is designed to grow. To add a new application:

1. Create a directory in the appropriate category (python-apps, web-apps, etc.)
2. Add an installation script in `scripts/install/`
3. Update this README

## License

Personal collection - use at your own discretion.

## Author

Dovendyr
