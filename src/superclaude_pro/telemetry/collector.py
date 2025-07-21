"""Telemetry collector for anonymous usage statistics."""

import json
import platform
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import structlog

from ..core.config import Config
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TelemetryCollector:
    """Collects anonymous telemetry data if enabled."""
    
    def __init__(self, config: Config) -> None:
        """Initialize telemetry collector.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.enabled = config.get("settings.telemetry", False)
        self.session_id = str(uuid.uuid4())
        self.metrics_file = config.claude_dir / ".telemetry" / "metrics.json"
        
        if self.enabled:
            self._ensure_telemetry_dir()
            self._load_or_create_client_id()
            logger.info("Telemetry enabled", session_id=self.session_id)
        else:
            logger.debug("Telemetry disabled")
    
    def _ensure_telemetry_dir(self) -> None:
        """Ensure telemetry directory exists."""
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_or_create_client_id(self) -> None:
        """Load or create anonymous client ID."""
        client_id_file = self.config.claude_dir / ".telemetry" / "client_id"
        
        if client_id_file.exists():
            self.client_id = client_id_file.read_text().strip()
        else:
            self.client_id = str(uuid.uuid4())
            client_id_file.write_text(self.client_id)
    
    def track_event(
        self,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Track an event.
        
        Args:
            event_name: Name of the event
            properties: Optional event properties
        """
        if not self.enabled:
            return
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "client_id": self.client_id,
            "event": event_name,
            "properties": properties or {},
            "context": self._get_context(),
        }
        
        self._store_event(event)
        logger.debug("Event tracked", event=event_name)
    
    def track_command(
        self,
        command: str,
        success: bool = True,
        duration_ms: Optional[int] = None,
    ) -> None:
        """Track command usage.
        
        Args:
            command: Command name
            success: Whether command succeeded
            duration_ms: Command execution time in milliseconds
        """
        self.track_event(
            "command_executed",
            {
                "command": command,
                "success": success,
                "duration_ms": duration_ms,
            },
        )
    
    def track_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Track an error.
        
        Args:
            error_type: Type of error
            error_message: Error message (sanitized)
            context: Optional error context
        """
        self.track_event(
            "error_occurred",
            {
                "error_type": error_type,
                "error_message": self._sanitize_error(error_message),
                "context": context or {},
            },
        )
    
    def _get_context(self) -> Dict[str, Any]:
        """Get telemetry context.
        
        Returns:
            Context dictionary
        """
        return {
            "version": self.config.version,
            "python_version": platform.python_version(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "profile": self.config.get("profile", "unknown"),
        }
    
    def _sanitize_error(self, error_message: str) -> str:
        """Sanitize error message to remove sensitive data.
        
        Args:
            error_message: Original error message
            
        Returns:
            Sanitized error message
        """
        # Remove file paths
        import re
        sanitized = re.sub(r'[\/]\S+[\/]\S+', '<path>', error_message)
        
        # Remove potential secrets (basic patterns)
        sanitized = re.sub(r'[a-zA-Z0-9]{20,}', '<redacted>', sanitized)
        
        # Limit length
        return sanitized[:500]
    
    def _store_event(self, event: Dict[str, Any]) -> None:
        """Store event locally.
        
        Args:
            event: Event data
        """
        try:
            # Read existing events
            if self.metrics_file.exists():
                with open(self.metrics_file, "r") as f:
                    events = json.load(f)
            else:
                events = []
            
            # Add new event
            events.append(event)
            
            # Keep only last 1000 events
            if len(events) > 1000:
                events = events[-1000:]
            
            # Write back
            with open(self.metrics_file, "w") as f:
                json.dump(events, f, indent=2)
        except Exception as e:
            logger.debug("Failed to store telemetry", error=str(e))
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics.
        
        Returns:
            Metrics summary
        """
        if not self.enabled or not self.metrics_file.exists():
            return {}
        
        try:
            with open(self.metrics_file, "r") as f:
                events = json.load(f)
            
            # Calculate summary
            command_counts = {}
            error_counts = {}
            total_commands = 0
            total_errors = 0
            
            for event in events:
                if event["event"] == "command_executed":
                    cmd = event["properties"]["command"]
                    command_counts[cmd] = command_counts.get(cmd, 0) + 1
                    total_commands += 1
                elif event["event"] == "error_occurred":
                    err_type = event["properties"]["error_type"]
                    error_counts[err_type] = error_counts.get(err_type, 0) + 1
                    total_errors += 1
            
            return {
                "total_events": len(events),
                "total_commands": total_commands,
                "total_errors": total_errors,
                "top_commands": sorted(
                    command_counts.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:10],
                "top_errors": sorted(
                    error_counts.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:5],
            }
        except Exception as e:
            logger.debug("Failed to get metrics summary", error=str(e))
            return {}