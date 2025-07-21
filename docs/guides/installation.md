# Installation Guide

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Claude Code**: Already installed and configured
- **Operating System**: Linux, macOS, or Windows
- **Git** (optional): For development installation

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Using pip
pip install superclaude-pro

# Or using uv (faster)
uv pip install superclaude-pro

# Run the installer
superclaude-pro install
```

### Method 2: Install from GitHub

```bash
# Clone the repository
git clone https://github.com/NUbem000/SuperClaude-Pro.git
cd SuperClaude-Pro

# Install in editable mode
pip install -e .

# Run the installer
superclaude-pro install
```

### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/NUbem000/SuperClaude-Pro.git
cd SuperClaude-Pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with all development dependencies
pip install -e ".[dev,docs,telemetry]"

# Install pre-commit hooks
pre-commit install

# Run the installer
superclaude-pro install --profile developer
```

## 🎯 Installation Profiles

### Quick Profile (Default)
```bash
superclaude-pro install --profile quick
```
- ✅ Essential commands
- ✅ Core personas
- ✅ Basic MCP servers
- ✅ Minimal configuration

### Minimal Profile
```bash
superclaude-pro install --profile minimal
```
- ✅ Core commands only
- ✅ No personas
- ✅ No MCP servers
- ✅ Lightweight installation

### Developer Profile
```bash
superclaude-pro install --profile developer
```
- ✅ All commands
- ✅ All personas
- ✅ All MCP servers
- ✅ Debug features
- ✅ Telemetry enabled

### Custom Profile
```bash
superclaude-pro install --profile custom
```
- Interactive selection of components
- Choose specific commands
- Select desired personas
- Pick MCP servers

## 📁 Installation Locations

SuperClaude Pro installs files in:

```
~/.claude/
├── superclaude.json      # Configuration file
├── commands/
│   └── sc/               # Command definitions
│       ├── analyze.md
│       ├── build.md
│       ├── implement.md
│       └── ...
├── personas/             # AI personas
│   ├── architect.md
│   ├── frontend.md
│   └── ...
├── CLAUDE.md             # Main configuration
├── COMMANDS.md           # Command system
├── PERSONAS.md           # Persona system
└── MCP.md                # MCP configuration
```

## ⚙️ Post-Installation Setup

### 1. Verify Installation

```bash
# Check status
superclaude-pro status

# Expected output:
# ✓ SuperClaude Pro installed
# Version: 3.1.0
# Profile: quick
# Components: commands, personas, mcp, orchestrator
```

### 2. Restart Claude Code

**Important**: You must restart Claude Code after installation for changes to take effect.

### 3. Test Commands

In Claude Code, try:
```
/sc:analyze
Hello! Let's test if SuperClaude Pro is working.
```

### 4. Configure Settings (Optional)

Edit `~/.claude/superclaude.json`:

```json
{
  "version": "3.1.0",
  "profile": "quick",
  "settings": {
    "auto_update": true,
    "telemetry": false,
    "debug": false
  },
  "mcp_servers": [
    "context7",
    "sequential",
    "magic",
    "playwright"
  ]
}
```

## 🔄 Updating

### Check for Updates
```bash
superclaude-pro update --check
```

### Update to Latest Version
```bash
# Update the package
pip install --upgrade superclaude-pro

# Run the update command
superclaude-pro update
```

## 🗑️ Uninstallation

### Complete Uninstall
```bash
# Remove SuperClaude Pro
superclaude-pro uninstall

# Uninstall the package
pip uninstall superclaude-pro
```

### Partial Uninstall
```bash
# Disable specific components
superclaude-pro component mcp --disable
superclaude-pro component personas --disable
```

## 🐛 Troubleshooting

### Commands Not Working

1. **Restart Claude Code**
   - Commands only load on startup
   - Full restart required (not reload)

2. **Check Installation**
   ```bash
   superclaude-pro status
   ls ~/.claude/commands/sc/
   ```

3. **Verify Path**
   ```bash
   which superclaude-pro
   python -m superclaude_pro --version
   ```

### Permission Errors

```bash
# Fix permissions
chmod -R 755 ~/.claude

# Never use sudo for pip install
# If you did, fix ownership:
chown -R $USER:$USER ~/.claude
```

### Import Errors

```bash
# Reinstall with all dependencies
pip install --force-reinstall superclaude-pro[dev,telemetry]

# Check Python version
python --version  # Must be 3.8+
```

### MCP Server Issues

1. **Check MCP configuration**
   ```bash
   cat ~/.claude/MCP.md
   ```

2. **Verify server availability**
   - Some MCP servers require additional setup
   - Check server-specific documentation

## 🏢 Enterprise Installation

### System-Wide Installation

```bash
# For all users (requires admin)
sudo pip install superclaude-pro

# Configure for specific user
superclaude-pro install --claude-dir /etc/claude
```

### Offline Installation

```bash
# Download wheel file
pip download superclaude-pro --no-deps -d .

# Transfer to offline machine
# Install from wheel
pip install superclaude_pro-*.whl
```

### Proxy Configuration

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Install through proxy
pip install superclaude-pro
```

## 📞 Getting Help

- **Documentation**: [Full Docs](https://github.com/NUbem000/SuperClaude-Pro/tree/main/docs)
- **Issues**: [GitHub Issues](https://github.com/NUbem000/SuperClaude-Pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NUbem000/SuperClaude-Pro/discussions)
- **Discord**: [Community Chat](https://discord.gg/superclaude)

---

**Next**: [Quickstart Guide](quickstart.md) →