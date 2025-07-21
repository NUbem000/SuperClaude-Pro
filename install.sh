#!/usr/bin/env bash

# SuperClaude Pro - Quick Installation Script
# https://github.com/NUbem000/SuperClaude-Pro

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   SuperClaude Pro                         ║"
echo "║         Professional Claude Code Extension                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo -e "${RED}Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# Check if Claude directory exists
CLAUDE_DIR="$HOME/.claude"
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${YELLOW}Warning: Claude directory not found at $CLAUDE_DIR${NC}"
    echo -e "${YELLOW}Make sure Claude Code is installed first${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip is not installed${NC}"
    echo "Please install pip first:"
    echo "  sudo apt-get install python3-pip  # On Ubuntu/Debian"
    echo "  brew install python3               # On macOS"
    exit 1
fi

PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

# Installation method selection
echo -e "\n${BLUE}Select installation method:${NC}"
echo "1) Quick install from PyPI (recommended)"
echo "2) Install from this repository"
echo "3) Development install"
read -p "Choice (1-3): " -n 1 -r
echo

case $REPLY in
    1)
        echo -e "\n${BLUE}Installing SuperClaude Pro from PyPI...${NC}"
        $PIP_CMD install --upgrade superclaude-pro
        ;;
    2)
        echo -e "\n${BLUE}Installing from repository...${NC}"
        $PIP_CMD install --upgrade .
        ;;
    3)
        echo -e "\n${BLUE}Installing in development mode...${NC}"
        $PIP_CMD install --upgrade -e ".[dev,docs,telemetry]"
        echo -e "${BLUE}Installing pre-commit hooks...${NC}"
        pre-commit install || echo -e "${YELLOW}Warning: pre-commit not installed${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Profile selection
echo -e "\n${BLUE}Select installation profile:${NC}"
echo "1) Quick - Essential features (default)"
echo "2) Minimal - Core commands only"
echo "3) Developer - All features + debug tools"
echo "4) Custom - Choose components"
read -p "Choice (1-4) [1]: " -n 1 -r
echo

PROFILE="quick"
case $REPLY in
    2) PROFILE="minimal" ;;
    3) PROFILE="developer" ;;
    4) PROFILE="custom" ;;
esac

# Run SuperClaude Pro installer
echo -e "\n${BLUE}Running SuperClaude Pro installer...${NC}"
if superclaude-pro install --profile "$PROFILE"; then
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ SuperClaude Pro installed successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${YELLOW}⚠️  Important: Restart Claude Code for changes to take effect${NC}"
    echo
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Restart Claude Code"
    echo "2. Try a command: /sc:analyze"
    echo "3. Read the docs: https://github.com/NUbem000/SuperClaude-Pro/tree/main/docs"
    echo
    echo -e "${BLUE}Useful commands:${NC}"
    echo "  superclaude-pro status    # Check installation"
    echo "  superclaude-pro update    # Update to latest version"
    echo "  superclaude-pro --help    # See all options"
else
    echo -e "\n${RED}Installation failed!${NC}"
    echo "Please check the error messages above."
    echo "For help, visit: https://github.com/NUbem000/SuperClaude-Pro/issues"
    exit 1
fi