"""Tests for configuration management."""

import json
from pathlib import Path

import pytest

from superclaude_pro.core.config import Config


class TestConfig:
    """Test Config class."""
    
    def test_init_creates_claude_dir(self, temp_dir: Path):
        """Test that initialization creates the Claude directory."""
        claude_dir = temp_dir / ".claude"
        assert not claude_dir.exists()
        
        config = Config(claude_dir=claude_dir)
        assert claude_dir.exists()
        assert claude_dir.is_dir()
    
    def test_load_returns_defaults_when_no_config(self, config: Config):
        """Test loading returns defaults when no config file exists."""
        result = config.load()
        defaults = config.get_defaults()
        
        assert result == defaults
        assert result["version"] == "3.1.0"
        assert result["profile"] == "quick"
    
    def test_save_and_load(self, config: Config):
        """Test saving and loading configuration."""
        test_config = {
            "version": "3.1.0",
            "profile": "developer",
            "custom_setting": "test_value"
        }
        
        config.save(test_config)
        loaded = config.load()
        
        assert loaded == test_config
        assert config.config_path.exists()
    
    def test_get_simple_key(self, config: Config):
        """Test getting a simple configuration value."""
        test_config = {"test_key": "test_value"}
        config.save(test_config)
        
        assert config.get("test_key") == "test_value"
        assert config.get("missing_key", "default") == "default"
    
    def test_get_nested_key(self, config: Config):
        """Test getting nested configuration values."""
        test_config = {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                }
            }
        }
        config.save(test_config)
        
        assert config.get("level1.level2.level3") == "deep_value"
        assert config.get("level1.level2") == {"level3": "deep_value"}
        assert config.get("level1.missing.key", "default") == "default"
    
    def test_set_simple_key(self, config: Config):
        """Test setting a simple configuration value."""
        config.set("new_key", "new_value")
        
        loaded = config.load()
        assert loaded["new_key"] == "new_value"
    
    def test_set_nested_key(self, config: Config):
        """Test setting nested configuration values."""
        config.set("level1.level2.level3", "deep_value")
        
        loaded = config.load()
        assert loaded["level1"]["level2"]["level3"] == "deep_value"
    
    def test_get_component_path(self, config: Config):
        """Test getting component paths."""
        commands_path = config.get_component_path("commands")
        assert commands_path == config.claude_dir / "commands" / "sc"
        
        personas_path = config.get_component_path("personas")
        assert personas_path == config.claude_dir / "personas"
        
        with pytest.raises(ValueError, match="Unknown component"):
            config.get_component_path("invalid_component")
    
    def test_is_installed(self, config: Config):
        """Test checking if SuperClaude Pro is installed."""
        assert not config.is_installed()
        
        config.save(config.get_defaults())
        assert config.is_installed()
    
    def test_get_installed_components(self, config: Config):
        """Test getting list of installed components."""
        test_config = {
            "components": {
                "commands": True,
                "personas": False,
                "mcp": True,
            }
        }
        config.save(test_config)
        
        components = config.get_installed_components()
        assert "commands" in components
        assert "personas" not in components
        assert "mcp" in components
    
    def test_config_file_corruption_handling(self, config: Config):
        """Test handling of corrupted config files."""
        # Write invalid JSON
        with open(config.config_path, "w") as f:
            f.write("{ invalid json }")
        
        # Should return defaults instead of crashing
        result = config.load()
        assert result == config.get_defaults()