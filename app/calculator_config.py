"""Configuration management for the calculator application."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages configuration settings for the calculator."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration with default values."""
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Base directories
        self.log_dir = Path(os.getenv('CALCULATOR_LOG_DIR', 'logs'))
        self.history_dir = Path(os.getenv('CALCULATOR_HISTORY_DIR', 'history'))
        
        # History settings
        self.max_history_size = self._get_int_config('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = self._get_bool_config('CALCULATOR_AUTO_SAVE', True)
        
        # Calculation settings
        self.precision = self._get_int_config('CALCULATOR_PRECISION', 2)
        self.max_input_value = self._get_float_config('CALCULATOR_MAX_INPUT_VALUE', 1000000.0)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        
        # Validate and create directories
        self._validate_config()
        self._create_directories()
    
    def _get_int_config(self, key: str, default: int) -> int:
        """Get integer configuration value with validation."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError as e:
            raise ConfigurationError(key, f"Invalid integer value for {key}: {os.getenv(key)}") from e
    
    def _get_float_config(self, key: str, default: float) -> float:
        """Get float configuration value with validation."""
        try:
            return float(os.getenv(key, str(default)))
        except ValueError as e:
            raise ConfigurationError(key, f"Invalid float value for {key}: {os.getenv(key)}") from e
    
    def _get_bool_config(self, key: str, default: bool) -> bool:
        """Get boolean configuration value with validation."""
        value = os.getenv(key, str(default)).lower()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
        else:
            raise ConfigurationError(key, f"Invalid boolean value for {key}: {value}")
    
    def _validate_config(self):
        """Validate configuration values."""
        if self.max_history_size <= 0:
            raise ConfigurationError("CALCULATOR_MAX_HISTORY_SIZE", "Max history size must be positive")
        
        if self.precision < 0:
            raise ConfigurationError("CALCULATOR_PRECISION", "Precision cannot be negative")
        
        if self.max_input_value <= 0:
            raise ConfigurationError("CALCULATOR_MAX_INPUT_VALUE", "Max input value must be positive")
        
        if self.precision > 10:
            raise ConfigurationError("CALCULATOR_PRECISION", "Precision cannot exceed 10 decimal places")
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.history_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ConfigurationError("directory_creation", f"Failed to create directories: {e}") from e
    
    @property
    def log_file(self) -> Path:
        """Get the log file path."""
        return self.log_dir / "calculator.log"
    
    @property
    def history_file(self) -> Path:
        """Get the history file path."""
        return self.history_dir / "calculation_history.csv"
    
    def get_summary(self) -> dict:
        """Get a summary of current configuration."""
        return {
            'log_dir': str(self.log_dir),
            'history_dir': str(self.history_dir),
            'max_history_size': self.max_history_size,
            'auto_save': self.auto_save,
            'precision': self.precision,
            'max_input_value': self.max_input_value,
            'default_encoding': self.default_encoding,
            'log_file': str(self.log_file),
            'history_file': str(self.history_file)
        }
