#!/bin/bash
# Installation script for Ollama Chat Application

set -e

echo "================================================"
echo "  Ollama Chat Application Setup"
echo "================================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS"
    exit 1
fi

echo "Detected OS: $OS"

# Install Python3 and Tkinter based on OS
echo "Installing dependencies..."

case $OS in
    ubuntu|debian)
        sudo apt update
        sudo apt install -y python3 python3-pip python3-tk
        ;;
    fedora)
        sudo dnf install -y python3 python3-pip python3-tkinter
        ;;
    centos|rhel)
        sudo yum install -y python3 python3-pip python3-tkinter
        ;;
    arch)
        sudo pacman -S --noconfirm python python-pip tk
        ;;
    opensuse*)
        sudo zypper install -y python3 python3-pip python3-tk
        ;;
    *)
        echo "Unsupported OS: $OS"
        echo "Please install Python 3, pip, and Tkinter manually"
        exit 1
        ;;
esac

# Install Python dependencies
echo "Installing Python packages..."
pip3 install --user requests

# Check if Ollama is installed
echo ""
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
    ollama --version
else
    echo "⚠ Ollama is not installed"
    echo ""
    echo "To install Ollama, run:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    read -p "Would you like to install Ollama now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "You can run the chat app, but you'll need Ollama installed to use it."
    fi
fi

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To run the Ollama Chat application:"
echo "  cd $ROOT_DIR/python-apps/ollama-chat"
echo "  python3 ollama_chat.py"
echo ""
echo "Note: Make sure Ollama is running (ollama serve)"
echo ""
