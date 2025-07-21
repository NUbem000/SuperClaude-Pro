"""Optional telemetry module for SuperClaude Pro."""

from typing import Optional

try:
    from .collector import TelemetryCollector
    from .metrics import Metrics
    TELEMETRY_AVAILABLE = True
except ImportError:
    TELEMETRY_AVAILABLE = False
    TelemetryCollector = None
    Metrics = None

__all__ = ["TelemetryCollector", "Metrics", "TELEMETRY_AVAILABLE"]