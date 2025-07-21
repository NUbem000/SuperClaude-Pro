"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from superclaude_pro.core.config import Config


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_claude_dir(temp_dir: Path) -> Path:
    """Create a mock Claude directory."""
    claude_dir = temp_dir / ".claude"
    claude_dir.mkdir()
    return claude_dir


@pytest.fixture
def config(mock_claude_dir: Path) -> Config:
    """Create a test configuration."""
    return Config(claude_dir=mock_claude_dir)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_home_dir(monkeypatch, temp_dir: Path) -> Path:
    """Mock the home directory."""
    home = temp_dir / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: home)
    return home


@pytest.fixture(autouse=True)
def isolate_tests(monkeypatch, temp_dir: Path):
    """Isolate tests from the real filesystem."""
    # Change to temp directory
    monkeypatch.chdir(temp_dir)
    
    # Set environment variables
    monkeypatch.setenv("SUPERCLAUDE_TEST_MODE", "1")
    monkeypatch.setenv("HOME", str(temp_dir))
    
    # Ensure we don't accidentally modify real files
    real_home = Path.home()
    
    def safe_mkdir(self, *args, **kwargs):
        if str(self).startswith(str(real_home)) and str(temp_dir) not in str(self):
            raise RuntimeError(f"Test tried to create directory in real home: {self}")
        return Path.mkdir(self, *args, **kwargs)
    
    monkeypatch.setattr(Path, "mkdir", safe_mkdir)