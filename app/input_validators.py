"""Input validation utilities for the calculator."""

import re
from typing import Union, Tuple
from app.exceptions import ValidationError


class InputValidator:
    """Validates user inputs for the calculator."""
    
    def __init__(self, max_value: float = 1000000.0, precision: int = 2):
        """Initialize validator with limits."""
        self.max_value = max_value
        self.precision = precision
    
    def validate_number(self, value: str) -> float:
        """Validate and convert string input to float."""
        if not value or not value.strip():
            raise ValidationError(value, "Input cannot be empty")
        
        # Remove whitespace
        value = value.strip()
        
        # Check for valid number format
        if not re.match(r'^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$', value):
            raise ValidationError(value, "Invalid number format")
        
        try:
            number = float(value)
        except ValueError as e:
            raise ValidationError(value, "Cannot convert to number") from e
        
        # Check for infinity and NaN
        if not self._is_finite(number):
            raise ValidationError(value, "Number must be finite")
        
        # Check range
        if abs(number) > self.max_value:
            raise ValidationError(value, f"Number exceeds maximum allowed value: {self.max_value}")
        
        return number
    
    def validate_operation_inputs(self, operand1: str, operand2: str) -> Tuple[float, float]:
        """Validate two operands for binary operations."""
        num1 = self.validate_number(operand1)
        num2 = self.validate_number(operand2)
        return num1, num2
    
    def validate_division(self, dividend: str, divisor: str) -> Tuple[float, float]:
        """Validate inputs for division operations."""
        num1, num2 = self.validate_operation_inputs(dividend, divisor)
        
        if num2 == 0:
            raise ValidationError(divisor, "Division by zero is not allowed")
        
        return num1, num2
    
    def validate_root(self, number: str, root: str) -> Tuple[float, float]:
        """Validate inputs for root operations."""
        num, root_val = self.validate_operation_inputs(number, root)
        
        if root_val == 0:
            raise ValidationError(root, "Root cannot be zero")
        
        if num < 0 and root_val % 2 == 0:
            raise ValidationError(number, "Cannot calculate even root of negative number")
        
        return num, root_val
    
    def validate_power(self, base: str, exponent: str) -> Tuple[float, float]:
        """Validate inputs for power operations."""
        base_val, exp_val = self.validate_operation_inputs(base, exponent)
        
        # Check for potential overflow
        if abs(base_val) > 1 and abs(exp_val) > 100:
            raise ValidationError(exponent, "Exponent too large, may cause overflow")
        
        if base_val == 0 and exp_val < 0:
            raise ValidationError(base, "Cannot raise zero to negative power")
        
        return base_val, exp_val
    
    def _is_finite(self, number: float) -> bool:
        """Check if number is finite (not infinity or NaN)."""
        import math
        return math.isfinite(number)
    
    def format_result(self, result: float) -> str:
        """Format calculation result according to precision settings."""
        if self._is_finite(result):
            return f"{result:.{self.precision}f}".rstrip('0').rstrip('.')
        else:
            return str(result)
