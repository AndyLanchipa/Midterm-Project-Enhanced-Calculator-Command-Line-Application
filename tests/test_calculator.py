"""Test cases for calculation model and calculator core functionality."""

import pytest
from datetime import datetime
from app.calculation import Calculation
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError, OperationError, ValidationError


class TestCalculation:
    """Test calculation model."""
    
    def test_calculation_creation(self):
        """Test creating a calculation."""
        calc = Calculation(5.0, 3.0, "add", 8.0)
        assert calc.operand1 == 5.0
        assert calc.operand2 == 3.0
        assert calc.operation == "add"
        assert calc.result == 8.0
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_string_representation(self):
        """Test calculation string representation."""
        calc = Calculation(10.0, 2.0, "divide", 5.0)
        expected = "10.0 divide 2.0 = 5.0"
        assert str(calc) == expected
    
    def test_calculation_to_dict(self):
        """Test calculation serialization to dictionary."""
        calc = Calculation(7.0, 3.0, "subtract", 4.0)
        calc_dict = calc.to_dict()
        
        assert calc_dict["operand1"] == 7.0
        assert calc_dict["operand2"] == 3.0
        assert calc_dict["operation"] == "subtract"
        assert calc_dict["result"] == 4.0
        assert "timestamp" in calc_dict
    
    def test_calculation_from_dict(self):
        """Test calculation deserialization from dictionary."""
        data = {
            "operand1": 6.0,
            "operand2": 2.0,
            "operation": "multiply",
            "result": 12.0,
            "timestamp": "2023-01-01T12:00:00"
        }
        calc = Calculation.from_dict(data)
        
        assert calc.operand1 == 6.0
        assert calc.operand2 == 2.0
        assert calc.operation == "multiply"
        assert calc.result == 12.0
    
    def test_calculation_equality(self):
        """Test calculation equality comparison."""
        calc1 = Calculation(5.0, 3.0, "add", 8.0)
        calc2 = Calculation(5.0, 3.0, "add", 8.0)
        calc3 = Calculation(5.0, 3.0, "subtract", 2.0)
        
        assert calc1 == calc2
        assert calc1 != calc3


class TestCalculator:
    """Test calculator functionality."""
    
    def setup_method(self):
        """Set up test calculator."""
        self.config = CalculatorConfig()
        self.calculator = Calculator(self.config)
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        assert self.calculator is not None
        assert self.calculator.config is not None
        assert len(self.calculator.get_available_operations()) == 10
    
    def test_basic_calculations(self):
        """Test basic calculator operations."""
        # Test addition
        result = self.calculator.perform_calculation("add", "5", "3")
        assert result.result == 8.0
        
        # Test subtraction
        result = self.calculator.perform_calculation("subtract", "10", "4")
        assert result.result == 6.0
        
        # Test multiplication
        result = self.calculator.perform_calculation("multiply", "6", "7")
        assert result.result == 42.0
        
        # Test division
        result = self.calculator.perform_calculation("divide", "15", "3")
        assert result.result == 5.0
    
    def test_advanced_calculations(self):
        """Test advanced calculator operations."""
        # Test power
        result = self.calculator.perform_calculation("power", "2", "3")
        assert result.result == 8.0
        
        # Test root
        result = self.calculator.perform_calculation("root", "27", "3")
        assert abs(result.result - 3.0) < 0.0001
        
        # Test modulus
        result = self.calculator.perform_calculation("modulus", "10", "3")
        assert result.result == 1.0
        
        # Test percentage
        result = self.calculator.perform_calculation("percent", "25", "100")
        assert result.result == 25.0
    
    def test_calculation_history(self):
        """Test calculation history management."""
        # Perform some calculations
        self.calculator.perform_calculation("add", "5", "3")
        self.calculator.perform_calculation("multiply", "4", "6")
        
        history = self.calculator.get_history()
        assert len(history) == 2
        
        last_calc = self.calculator.get_last_calculation()
        assert last_calc.operation == "multiply"
        assert last_calc.result == 24.0
    
    def test_undo_redo_functionality(self):
        """Test undo and redo operations."""
        # Perform calculations
        self.calculator.perform_calculation("add", "5", "3")
        self.calculator.perform_calculation("subtract", "10", "2")
        
        assert len(self.calculator.get_history()) == 2
        
        # Test undo
        undo_success = self.calculator.undo()
        assert undo_success is True
        assert len(self.calculator.get_history()) == 1
        
        # Test redo
        redo_success = self.calculator.redo()
        assert redo_success is True
        assert len(self.calculator.get_history()) == 2
        
        # Test undo/redo limits
        self.calculator.undo()
        self.calculator.undo()
        further_undo = self.calculator.undo()
        assert further_undo is False
    
    def test_clear_history(self):
        """Test clearing calculation history."""
        self.calculator.perform_calculation("add", "1", "1")
        self.calculator.perform_calculation("add", "2", "2")
        
        assert len(self.calculator.get_history()) == 2
        
        self.calculator.clear_history()
        assert len(self.calculator.get_history()) == 0
    
    def test_invalid_operation(self):
        """Test handling of invalid operations."""
        with pytest.raises(OperationError):
            self.calculator.perform_calculation("invalid_op", "5", "3")
    
    def test_invalid_input_validation(self):
        """Test input validation errors."""
        with pytest.raises(ValidationError):
            self.calculator.perform_calculation("add", "abc", "3")
        
        with pytest.raises(ValidationError):
            self.calculator.perform_calculation("add", "5", "")
        
        with pytest.raises(ValidationError):
            self.calculator.perform_calculation("divide", "5", "0")
    
    def test_calculator_info(self):
        """Test calculator information retrieval."""
        info = self.calculator.get_calculator_info()
        
        assert "precision" in info
        assert "max_input_value" in info
        assert "available_operations" in info
        assert len(info["available_operations"]) == 10
        assert info["history_count"] >= 0
    
    def test_observer_notification(self):
        """Test that observers are notified of calculations."""
        initial_observer_count = self.calculator.get_observer_count()
        assert initial_observer_count >= 1  # Should have logging observer
        
        # Perform calculation (should notify observers)
        self.calculator.perform_calculation("add", "2", "3")
        
        # Observer count should remain the same
        assert self.calculator.get_observer_count() == initial_observer_count
    
    def test_edge_case_calculations(self):
        """Test edge cases in calculations."""
        # Large numbers
        result = self.calculator.perform_calculation("add", "999999", "1")
        assert result.result == 1000000.0
        
        # Negative numbers
        result = self.calculator.perform_calculation("multiply", "-5", "3")
        assert result.result == -15.0
        
        # Decimal numbers
        result = self.calculator.perform_calculation("add", "2.5", "3.7")
        assert abs(result.result - 6.2) < 0.0001
    
    def test_precision_handling(self):
        """Test precision in calculation results."""
        # Test that results are formatted according to precision
        result = self.calculator.perform_calculation("divide", "1", "3")
        # Result should be formatted to configured precision
        assert isinstance(result.result, float)
