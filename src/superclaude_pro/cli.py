"""Command Line Interface for SuperClaude Pro."""

import sys
from pathlib import Path
from typing import Optional

import click
import structlog
from rich.console import Console
from rich.panel import Panel

from .core.config import Config
from .core.installer import Installer
from .utils.logger import setup_logging

logger = structlog.get_logger()
console = Console()


@click.group()
@click.version_option()
@click.option(
    "--debug", is_flag=True, help="Enable debug logging"
)
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    """SuperClaude Pro - Extend Claude Code with superpowers! 🚀"""
    setup_logging(debug=debug)
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug


@cli.command()
@click.option(
    "--profile",
    type=click.Choice(["minimal", "quick", "developer", "custom"]),
    default="quick",
    help="Installation profile to use",
)
@click.option(
    "--force", is_flag=True, help="Force reinstall even if already installed"
)
@click.option(
    "--claude-dir",
    type=click.Path(path_type=Path),
    help="Custom Claude configuration directory",
)
@click.pass_context
def install(ctx: click.Context, profile: str, force: bool, claude_dir: Optional[Path]) -> None:
    """Install SuperClaude Pro framework."""
    try:
        config = Config(claude_dir=claude_dir)
        installer = Installer(config=config, debug=ctx.obj["debug"])
        
        console.print(
            Panel.fit(
                f"[bold cyan]Installing SuperClaude Pro[/bold cyan]\n"
                f"Profile: [yellow]{profile}[/yellow]",
                border_style="cyan"
            )
        )
        
        installer.install(profile=profile, force=force)
        
        console.print(
            "\n[bold green]✓[/bold green] SuperClaude Pro installed successfully!"
        )
        console.print(
            "\n[dim]Run [bold]superclaude-pro help[/bold] to see available commands.[/dim]"
        )
    except Exception as e:
        logger.exception("Installation failed")
        console.print(f"\n[bold red]✗ Installation failed:[/bold red] {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--check", is_flag=True, help="Check for updates without installing"
)
@click.pass_context
def update(ctx: click.Context, check: bool) -> None:
    """Update SuperClaude Pro to the latest version."""
    try:
        config = Config()
        installer = Installer(config=config, debug=ctx.obj["debug"])
        
        if check:
            update_available = installer.check_for_updates()
            if update_available:
                console.print("[yellow]⚠[/yellow] Update available!")
            else:
                console.print("[green]✓[/green] You're on the latest version.")
        else:
            installer.update()
            console.print("[green]✓[/green] Updated successfully!")
    except Exception as e:
        logger.exception("Update failed")
        console.print(f"[red]✗ Update failed:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to uninstall?")
def uninstall() -> None:
    """Uninstall SuperClaude Pro framework."""
    try:
        config = Config()
        installer = Installer(config=config)
        installer.uninstall()
        console.print("[green]✓[/green] Uninstalled successfully!")
    except Exception as e:
        logger.exception("Uninstall failed")
        console.print(f"[red]✗ Uninstall failed:[/red] {e}")
        sys.exit(1)


@cli.command()
def status() -> None:
    """Show SuperClaude Pro installation status."""
    try:
        config = Config()
        installer = Installer(config=config)
        status_info = installer.get_status()
        
        console.print(
            Panel(
                f"[bold]SuperClaude Pro Status[/bold]\n\n"
                f"Installed: {status_info['installed']}\n"
                f"Version: {status_info['version']}\n"
                f"Profile: {status_info['profile']}\n"
                f"Components: {', '.join(status_info['components'])}",
                border_style="cyan"
            )
        )
    except Exception as e:
        logger.exception("Failed to get status")
        console.print(f"[red]✗ Failed to get status:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.argument("component")
@click.option("--enable/--disable", default=True, help="Enable or disable component")
def component(component: str, enable: bool) -> None:
    """Manage individual components."""
    try:
        config = Config()
        installer = Installer(config=config)
        
        if enable:
            installer.enable_component(component)
            console.print(f"[green]✓[/green] Enabled {component}")
        else:
            installer.disable_component(component)
            console.print(f"[yellow]⚠[/yellow] Disabled {component}")
    except Exception as e:
        logger.exception(f"Failed to {'enable' if enable else 'disable'} component")
        console.print(f"[red]✗ Operation failed:[/red] {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()