"""Tests for CLI commands."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from superclaude_pro.cli import cli


class TestCLI:
    """Test CLI commands."""
    
    def test_cli_version(self, cli_runner: CliRunner):
        """Test version option."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()
    
    def test_cli_help(self, cli_runner: CliRunner):
        """Test help output."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "SuperClaude Pro" in result.output
        assert "install" in result.output
        assert "update" in result.output
        assert "uninstall" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_install_command_default(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test install command with defaults."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["install"])
        
        assert result.exit_code == 0
        mock_installer.install.assert_called_once_with(profile="quick", force=False)
        assert "installed successfully" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_install_command_with_options(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test install command with options."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["install", "--profile", "developer", "--force"])
        
        assert result.exit_code == 0
        mock_installer.install.assert_called_once_with(profile="developer", force=True)
    
    @patch("superclaude_pro.cli.Installer")
    def test_install_command_failure(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test install command when installation fails."""
        mock_installer = Mock()
        mock_installer.install.side_effect = Exception("Installation error")
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["install"])
        
        assert result.exit_code == 1
        assert "Installation failed" in result.output
        assert "Installation error" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_update_command(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test update command."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["update"])
        
        assert result.exit_code == 0
        mock_installer.update.assert_called_once()
        assert "Updated successfully" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_update_check_only(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test update command with --check flag."""
        mock_installer = Mock()
        mock_installer.check_for_updates.return_value = True
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["update", "--check"])
        
        assert result.exit_code == 0
        mock_installer.check_for_updates.assert_called_once()
        mock_installer.update.assert_not_called()
        assert "Update available" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_uninstall_command_confirmed(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test uninstall command with confirmation."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["uninstall"], input="y\n")
        
        assert result.exit_code == 0
        mock_installer.uninstall.assert_called_once()
        assert "Uninstalled successfully" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_uninstall_command_cancelled(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test uninstall command when cancelled."""
        result = cli_runner.invoke(cli, ["uninstall"], input="n\n")
        
        assert result.exit_code == 1
        assert "Aborted" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_status_command(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test status command."""
        mock_installer = Mock()
        mock_installer.get_status.return_value = {
            "installed": True,
            "version": "3.1.0",
            "profile": "developer",
            "components": ["commands", "personas", "mcp"]
        }
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["status"])
        
        assert result.exit_code == 0
        assert "SuperClaude Pro Status" in result.output
        assert "3.1.0" in result.output
        assert "developer" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_component_enable(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test enabling a component."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["component", "mcp", "--enable"])
        
        assert result.exit_code == 0
        mock_installer.enable_component.assert_called_once_with("mcp")
        assert "Enabled mcp" in result.output
    
    @patch("superclaude_pro.cli.Installer")
    def test_component_disable(self, mock_installer_class: Mock, cli_runner: CliRunner):
        """Test disabling a component."""
        mock_installer = Mock()
        mock_installer_class.return_value = mock_installer
        
        result = cli_runner.invoke(cli, ["component", "mcp", "--disable"])
        
        assert result.exit_code == 0
        mock_installer.disable_component.assert_called_once_with("mcp")
        assert "Disabled mcp" in result.output