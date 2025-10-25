"""Logging system for the calculator application."""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation


class CalculatorLogger:
    """Logger class for calculator operations and events."""
    
    def __init__(self, config: CalculatorConfig, name: str = "calculator"):
        """Initialize logger with configuration."""
        self.config = config
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up file and console handlers."""
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler with rotation
        log_file = self.config.log_file
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding=self.config.default_encoding
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_calculation(self, calculation: Calculation) -> None:
        """Log a calculation operation."""
        message = (f"Calculation performed: {calculation.operand1} "
                  f"{calculation.operation} {calculation.operand2} = {calculation.result}")
        self.logger.info(message)
    
    def log_operation(self, operation: str, operand1: float, operand2: float, result: float) -> None:
        """Log an operation with details."""
        message = f"Operation: {operation}({operand1}, {operand2}) = {result}"
        self.logger.info(message)
    
    def log_error(self, operation: str, error_message: str, operand1: Optional[float] = None, 
                  operand2: Optional[float] = None) -> None:
        """Log an error during calculation."""
        if operand1 is not None and operand2 is not None:
            message = f"Error in {operation}({operand1}, {operand2}): {error_message}"
        else:
            message = f"Error in {operation}: {error_message}"
        self.logger.error(message)
    
    def log_history_action(self, action: str, details: str = "") -> None:
        """Log history-related actions."""
        message = f"History action: {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_config_action(self, action: str, details: str = "") -> None:
        """Log configuration-related actions."""
        message = f"Configuration: {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_user_action(self, action: str, details: str = "") -> None:
        """Log user interface actions."""
        message = f"User action: {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_system_event(self, event: str, details: str = "") -> None:
        """Log system events."""
        message = f"System event: {event}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def set_level(self, level: str) -> None:
        """Set logging level."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            self.logger.setLevel(level_map[level.upper()])
            self.log_config_action("Log level changed", f"New level: {level.upper()}")
        else:
            self.log_warning(f"Invalid log level: {level}")
    
    def get_log_file_path(self) -> Path:
        """Get the path to the log file."""
        return self.config.log_file
