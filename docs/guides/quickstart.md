# Quickstart Guide

## 🚀 Get Started in 5 Minutes

This guide will help you install and start using SuperClaude Pro quickly.

## Prerequisites

- Python 3.8 or higher
- Claude Code installed and configured
- Basic familiarity with command line

## Installation

### Option 1: Using uv (Recommended)

```bash
# Install SuperClaude Pro
uv pip install superclaude-pro

# Run the installer
superclaude-pro install
```

### Option 2: Using pip

```bash
# Install SuperClaude Pro
pip install superclaude-pro

# Run the installer
superclaude-pro install
```

## First Steps

### 1. Verify Installation

```bash
superclaude-pro status
```

You should see:
```
┌───────────────────────────────────────────────────────────────────────────┐
│ SuperClaude Pro Status                                           │
│                                                                  │
│ Installed: True                                                  │
│ Version: 3.1.0                                                   │
│ Profile: quick                                                   │
│ Components: commands, personas, mcp, orchestrator                │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2. Try Your First Command

In Claude Code, try these commands:

```
/sc:analyze
```
Analyze the current project structure and code quality.

```
/sc:explain main.py
```
Get a detailed explanation of a specific file.

```
/sc:implement "Add user authentication"
```
Implement a new feature with best practices.

### 3. Work with Personas

Personas automatically activate based on context:

```
"Design a REST API for user management"
```
The Architect persona will help with system design.

```
"Review this code for security issues"
```
The Security persona will perform a security audit.

## Basic Examples

### Code Analysis
```
/sc:analyze --metrics --suggestions
```

### Smart Implementation
```
/sc:implement "Add caching layer to improve performance"
```

### Testing
```
/sc:test --coverage --missing
```

### Documentation
```
/sc:document --format markdown --examples
```

## Configuration

SuperClaude Pro stores its configuration in `~/.claude/superclaude.json`:

```json
{
  "version": "3.1.0",
  "profile": "quick",
  "components": {
    "commands": true,
    "personas": true,
    "mcp": true,
    "orchestrator": true
  },
  "settings": {
    "auto_update": true,
    "telemetry": false,
    "debug": false
  }
}
```

## Next Steps

1. 📚 Read the [Commands Reference](commands.md) to learn all available commands
2. 🤖 Explore [Personas Guide](personas.md) for AI-powered assistance
3. 🔌 Learn about [MCP Integration](mcp.md) for external tools
4. 🌊 Discover [Wave Orchestration](orchestration.md) for complex tasks

## Troubleshooting

### Command not found
Make sure Claude Code is restarted after installation.

### Permission errors
```bash
sudo superclaude-pro install  # Not recommended
# Better: Fix permissions
chown -R $USER ~/.claude
```

### Import errors
Reinstall with all dependencies:
```bash
pip install --upgrade superclaude-pro[dev,telemetry]
```

## Getting Help

- Check the [FAQ](faq.md)
- Join our [Discord](https://discord.gg/superclaude)
- Create an [issue](https://github.com/NUbem000/SuperClaude-Pro/issues)

---

**Ready to supercharge your Claude Code experience? Let's go! 🚀**