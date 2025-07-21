"""Enhanced logging system for SuperClaude Pro."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from rich.console import Console
from rich.logging import RichHandler

# Global console instance
console = Console(stderr=True)


def setup_logging(
    debug: bool = False,
    log_file: Optional[Path] = None,
    json_logs: bool = False,
    correlation_id: Optional[str] = None,
) -> None:
    """Configure structured logging for SuperClaude Pro.
    
    Args:
        debug: Enable debug logging
        log_file: Optional log file path
        json_logs: Output logs in JSON format
        correlation_id: Optional correlation ID for request tracking
    """
    # Determine log level
    level = logging.DEBUG if debug else logging.INFO
    
    # Configure processors
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add correlation ID if provided
    if correlation_id:
        processors.append(
            structlog.processors.CallsiteParameterAdder(
                parameters=[structlog.processors.CallsiteParameter.THREAD_NAME],
                additional_ignores=["logging", "rich"],
            )
        )
        processors.insert(
            0,
            lambda _, __, event_dict: {
                **event_dict,
                "correlation_id": correlation_id,
            },
        )
    
    # Configure output format
    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        processors.append(structlog.dev.ConsoleRenderer())
        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=debug,
            markup=True,
        )
    
    # Configure Python's logging
    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        if json_logs:
            file_handler.setFormatter(logging.Formatter("%(message)s"))
        else:
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        logging.getLogger().addHandler(file_handler)
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Log initialization
    logger = structlog.get_logger()
    logger.info(
        "Logging initialized",
        level=logging.getLevelName(level),
        json_logs=json_logs,
        log_file=str(log_file) if log_file else None,
    )


def get_logger(name: Optional[str] = None, **kwargs: Any) -> structlog.BoundLogger:
    """Get a logger instance with optional context.
    
    Args:
        name: Logger name (defaults to module name)
        **kwargs: Additional context to bind to the logger
    
    Returns:
        Configured logger instance
    """
    logger = structlog.get_logger(name)
    
    if kwargs:
        logger = logger.bind(**kwargs)
    
    return logger


class LogContext:
    """Context manager for temporary log context."""
    
    def __init__(self, logger: structlog.BoundLogger, **kwargs: Any) -> None:
        """Initialize log context.
        
        Args:
            logger: Logger instance
            **kwargs: Context to temporarily bind
        """
        self.logger = logger
        self.context = kwargs
        self.token: Optional[Any] = None
    
    def __enter__(self) -> structlog.BoundLogger:
        """Enter context and bind values."""
        self.token = structlog.contextvars.bind_contextvars(**self.context)
        return self.logger
    
    def __exit__(self, *args: Any) -> None:
        """Exit context and unbind values."""
        if self.token:
            structlog.contextvars.unbind_contextvars(self.token)


def log_duration(func):
    """Decorator to log function execution duration."""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = datetime.now()
        
        try:
            logger.debug(f"Starting {func.__name__}", function=func.__name__)
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Completed {func.__name__}",
                function=func.__name__,
                duration_seconds=duration,
            )
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(
                f"Failed {func.__name__}",
                function=func.__name__,
                duration_seconds=duration,
                error=str(e),
                exc_info=True,
            )
            raise
    
    return wrapper


def log_errors(logger: Optional[structlog.BoundLogger] = None):
    """Decorator to log exceptions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_logger(func.__module__)
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}",
                    function=func.__name__,
                    error=str(e),
                    exc_info=True,
                )
                raise
        
        return wrapper
    return decorator