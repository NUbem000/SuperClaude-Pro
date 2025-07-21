"""Configuration management for SuperClaude Pro."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


@dataclass
class Config:
    """Configuration for SuperClaude Pro."""
    
    claude_dir: Path = field(default_factory=lambda: Path.home() / ".claude")
    config_file: str = "superclaude.json"
    version: str = "3.1.0"
    
    def __post_init__(self) -> None:
        """Initialize configuration."""
        self.claude_dir = Path(self.claude_dir)
        self.config_path = self.claude_dir / self.config_file
        self.ensure_claude_dir()
    
    def ensure_claude_dir(self) -> None:
        """Ensure Claude directory exists."""
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Ensured Claude directory exists", path=str(self.claude_dir))
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from disk."""
        if not self.config_path.exists():
            logger.debug("Config file not found, returning defaults")
            return self.get_defaults()
        
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            logger.debug("Loaded configuration", config=config)
            return config
        except Exception as e:
            logger.error("Failed to load config", error=str(e))
            return self.get_defaults()
    
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration to disk."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
            logger.debug("Saved configuration", config=config)
        except Exception as e:
            logger.error("Failed to save config", error=str(e))
            raise
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": self.version,
            "profile": "quick",
            "components": {
                "commands": True,
                "personas": True,
                "mcp": True,
                "orchestrator": True,
            },
            "settings": {
                "auto_update": True,
                "telemetry": False,
                "debug": False,
            },
            "mcp_servers": [
                "context7",
                "sequential",
                "magic",
                "playwright",
            ],
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        config = self.load()
        keys = key.split(".")
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        config = self.load()
        keys = key.split(".")
        
        # Navigate to the parent of the target key
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        self.save(config)
    
    def get_component_path(self, component: str) -> Path:
        """Get path for a component."""
        if component == "commands":
            return self.claude_dir / "commands" / "sc"
        elif component == "personas":
            return self.claude_dir / "personas"
        elif component == "mcp":
            return self.claude_dir / "mcp"
        elif component == "core":
            return self.claude_dir
        else:
            raise ValueError(f"Unknown component: {component}")
    
    def is_installed(self) -> bool:
        """Check if SuperClaude Pro is installed."""
        return self.config_path.exists()
    
    def get_installed_components(self) -> List[str]:
        """Get list of installed components."""
        config = self.load()
        components = config.get("components", {})
        return [name for name, enabled in components.items() if enabled]