"""Operation classes for the calculator."""

from abc import ABC, abstractmethod
import math
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all operations."""
    
    @abstractmethod
    def execute(self, operand1: float, operand2: float) -> float:
        """Execute the operation with two operands."""
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        """Return the symbol representing this operation."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Add two numbers."""
        return operand1 + operand2
    
    @property
    def symbol(self) -> str:
        return "+"
    
    @property
    def name(self) -> str:
        return "add"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Subtract second number from first."""
        return operand1 - operand2
    
    @property
    def symbol(self) -> str:
        return "-"
    
    @property
    def name(self) -> str:
        return "subtract"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Multiply two numbers."""
        return operand1 * operand2
    
    @property
    def symbol(self) -> str:
        return "*"
    
    @property
    def name(self) -> str:
        return "multiply"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Divide first number by second."""
        if operand2 == 0:
            raise OperationError("divide", "Cannot divide by zero")
        return operand1 / operand2
    
    @property
    def symbol(self) -> str:
        return "/"
    
    @property
    def name(self) -> str:
        return "divide"
