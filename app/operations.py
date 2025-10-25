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
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what this operation does."""
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
    
    @property
    def description(self) -> str:
        return "Add two numbers together"


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
    
    @property
    def description(self) -> str:
        return "Subtract second number from first number"


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
    
    @property
    def description(self) -> str:
        return "Multiply two numbers together"


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
    
    @property
    def description(self) -> str:
        return "Divide first number by second number"


class PowerOperation(Operation):
    """Power/exponentiation operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Raise first number to the power of second."""
        if operand1 == 0 and operand2 < 0:
            raise OperationError("power", "Cannot raise zero to negative power")
        
        try:
            result = operand1 ** operand2
            if not math.isfinite(result):
                raise OperationError("power", "Result is infinite or undefined")
            return result
        except OverflowError:
            raise OperationError("power", "Result too large to calculate")
    
    @property
    def symbol(self) -> str:
        return "^"
    
    @property
    def name(self) -> str:
        return "power"
    
    @property
    def description(self) -> str:
        return "Raise first number to the power of second number"


class RootOperation(Operation):
    """Root operation (nth root)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate nth root of first number."""
        if operand2 == 0:
            raise OperationError("root", "Root cannot be zero")
        
        if operand1 < 0 and operand2 % 2 == 0:
            raise OperationError("root", "Cannot calculate even root of negative number")
        
        try:
            if operand1 < 0:
                # For odd roots of negative numbers
                return -(abs(operand1) ** (1 / operand2))
            else:
                return operand1 ** (1 / operand2)
        except (OverflowError, ZeroDivisionError):
            raise OperationError("root", "Cannot calculate root")
    
    @property
    def symbol(self) -> str:
        return "√"
    
    @property
    def name(self) -> str:
        return "root"
    
    @property
    def description(self) -> str:
        return "Calculate nth root of first number (where n is second number)"


class ModulusOperation(Operation):
    """Modulus operation (remainder)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate remainder of division."""
        if operand2 == 0:
            raise OperationError("modulus", "Cannot calculate modulus with zero divisor")
        return operand1 % operand2
    
    @property
    def symbol(self) -> str:
        return "%"
    
    @property
    def name(self) -> str:
        return "modulus"
    
    @property
    def description(self) -> str:
        return "Calculate remainder when first number is divided by second number"


class IntegerDivideOperation(Operation):
    """Integer division operation (floor division)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Perform integer division."""
        if operand2 == 0:
            raise OperationError("int_divide", "Cannot divide by zero")
        return operand1 // operand2
    
    @property
    def symbol(self) -> str:
        return "//"
    
    @property
    def name(self) -> str:
        return "int_divide"
    
    @property
    def description(self) -> str:
        return "Perform integer division (floor division) of first number by second number"


class PercentageOperation(Operation):
    """Percentage calculation operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate what percentage operand1 is of operand2."""
        if operand2 == 0:
            raise OperationError("percent", "Cannot calculate percentage with zero base")
        return (operand1 / operand2) * 100
    
    @property
    def symbol(self) -> str:
        return "%of"
    
    @property
    def name(self) -> str:
        return "percent"
    
    @property
    def description(self) -> str:
        return "Calculate what percentage first number is of second number"


class AbsoluteDifferenceOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate absolute difference between two numbers."""
        return abs(operand1 - operand2)
    
    @property
    def symbol(self) -> str:
        return "abs_diff"
    
    @property
    def name(self) -> str:
        return "abs_diff"
    
    @property
    def description(self) -> str:
        return "Calculate absolute difference between two numbers"


class OperationFactory:
    """Factory class for creating operation instances using Factory Design Pattern."""
    
    _operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
        "modulus": ModulusOperation,
        "int_divide": IntegerDivideOperation,
        "percent": PercentageOperation,
        "abs_diff": AbsoluteDifferenceOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """Create an operation instance by name."""
        operation_name = operation_name.lower().strip()
        
        if operation_name not in cls._operations:
            available_ops = ", ".join(cls._operations.keys())
            raise OperationError(
                operation_name, 
                f"Unknown operation '{operation_name}'. Available operations: {available_ops}"
            )
        
        return cls._operations[operation_name]()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Get list of available operation names."""
        return list(cls._operations.keys())
    
    @classmethod
    def register_operation(cls, name: str, operation_class: type):
        """Register a new operation class (for extensibility)."""
        if not issubclass(operation_class, Operation):
            raise OperationError(name, "Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class


def calculate(operation_name: str, operand1: float, operand2: float) -> float:
    """Convenience function to perform a calculation."""
    operation = OperationFactory.create_operation(operation_name)
    return operation.execute(operand1, operand2)


def get_operation_symbol(operation_name: str) -> str:
    """Get the symbol for an operation."""
    operation = OperationFactory.create_operation(operation_name)
    return operation.symbol


def is_valid_operation(operation_name: str) -> bool:
    """Check if an operation name is valid."""
    return operation_name.lower().strip() in OperationFactory.get_available_operations()
