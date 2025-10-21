"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    
    def __init__(self, message: str, error_code: str = None):
        """Initialize calculator error with message and optional error code."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed."""
    
    def __init__(self, operation: str, message: str = None):
        """Initialize operation error with operation name and message."""
        if message is None:
            message = f"Cannot perform operation: {operation}"
        super().__init__(message, "OPERATION_ERROR")
        self.operation = operation


class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    
    def __init__(self, input_value: str, message: str = None):
        """Initialize validation error with input value and message."""
        if message is None:
            message = f"Invalid input: {input_value}"
        super().__init__(message, "VALIDATION_ERROR")
        self.input_value = input_value


class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""
    
    def __init__(self, config_key: str, message: str = None):
        """Initialize configuration error with config key and message."""
        if message is None:
            message = f"Invalid configuration for: {config_key}"
        super().__init__(message, "CONFIG_ERROR")
        self.config_key = config_key


class HistoryError(CalculatorError):
    """Raised when history operations fail."""
    
    def __init__(self, message: str):
        """Initialize history error with message."""
        super().__init__(message, "HISTORY_ERROR")


class FileOperationError(CalculatorError):
    """Raised when file operations fail."""
    
    def __init__(self, file_path: str, operation: str, message: str = None):
        """Initialize file operation error."""
        if message is None:
            message = f"Failed to {operation} file: {file_path}"
        super().__init__(message, "FILE_ERROR")
        self.file_path = file_path
        self.operation = operation
