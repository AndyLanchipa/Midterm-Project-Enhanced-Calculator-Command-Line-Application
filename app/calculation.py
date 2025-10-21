"""Core calculation model for the calculator."""

from datetime import datetime
from typing import Any, Dict


class Calculation:
    """Represents a single calculation with operands, operation, and result."""
    
    def __init__(self, operand1: float, operand2: float, operation: str, result: float):
        """Initialize a calculation instance."""
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation
        self.result = result
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        """String representation of the calculation."""
        return f"{self.operand1} {self.operation} {self.operand2} = {self.result}"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Calculation(operand1={self.operand1}, operand2={self.operand2}, "
                f"operation='{self.operation}', result={self.result}, "
                f"timestamp='{self.timestamp}')")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert calculation to dictionary for serialization."""
        return {
            'operand1': self.operand1,
            'operand2': self.operand2,
            'operation': self.operation,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Calculation':
        """Create calculation instance from dictionary."""
        calc = cls(
            operand1=data['operand1'],
            operand2=data['operand2'],
            operation=data['operation'],
            result=data['result']
        )
        # Set timestamp if available
        if 'timestamp' in data:
            calc.timestamp = datetime.fromisoformat(data['timestamp'])
        return calc
    
    def __eq__(self, other) -> bool:
        """Check if two calculations are equal."""
        if not isinstance(other, Calculation):
            return False
        return (self.operand1 == other.operand1 and
                self.operand2 == other.operand2 and
                self.operation == other.operation and
                self.result == other.result)
