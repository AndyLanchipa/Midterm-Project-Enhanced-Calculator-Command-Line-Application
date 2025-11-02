"""Additional tests to improve coverage."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from pathlib import Path
from app.calculation import Calculation
from app.operations import OperationFactory, is_valid_operation, get_operation_symbol
from app.exceptions import OperationError, ValidationError, ConfigurationError
from app.calculator_config import CalculatorConfig
from app.history import CalculationHistory


class TestOperationFactoryExtended:
    """Extended tests for operation factory."""
    
    def test_register_new_operation(self):
        """Test registering a new operation."""
        from app.operations import Operation
        
        class TestOperation(Operation):
            def execute(self, operand1: float, operand2: float) -> float:
                return operand1 + operand2 + 10
            
            @property
            def symbol(self) -> str:
                return "test"
            
            @property 
            def name(self) -> str:
                return "test_op"
            
            @property
            def description(self) -> str:
                return "Test operation"
        
        # Register new operation
        OperationFactory.register_operation("test_op", TestOperation)
        
        # Test it works
        operation = OperationFactory.create_operation("test_op")
        result = operation.execute(5, 3)
        assert result == 18  # 5 + 3 + 10
        
        # Clean up
        del OperationFactory._operations["test_op"]
    
    def test_register_invalid_operation(self):
        """Test registering invalid operation class."""
        class InvalidOperation:
            pass
        
        with pytest.raises(OperationError):
            OperationFactory.register_operation("invalid", InvalidOperation)
    
    def test_utility_functions(self):
        """Test utility functions."""
        assert is_valid_operation("add") == True
        assert is_valid_operation("invalid") == False
        
        symbol = get_operation_symbol("add")
        assert symbol == "+"
        
        operations = OperationFactory.get_available_operations()
        assert isinstance(operations, list)
        assert "add" in operations


class TestCalculationExtended:
    """Extended tests for Calculation class."""
    
    def test_calculation_to_dict(self):
        """Test calculation to dictionary conversion."""
        calc = Calculation(5.0, 3.0, "add", 8.0)
        data = calc.to_dict()
        
        assert data['operand1'] == 5.0
        assert data['operand2'] == 3.0
        assert data['operation'] == "add"
        assert data['result'] == 8.0
        assert 'timestamp' in data
    
    def test_calculation_from_dict(self):
        """Test calculation from dictionary creation."""
        data = {
            'operand1': 10.0,
            'operand2': 5.0,
            'operation': 'subtract',
            'result': 5.0,
            'timestamp': '2023-01-01T12:00:00'
        }
        
        calc = Calculation.from_dict(data)
        assert calc.operand1 == 10.0
        assert calc.operand2 == 5.0
        assert calc.operation == "subtract"
        assert calc.result == 5.0
    
    def test_calculation_repr(self):
        """Test calculation repr method."""
        calc = Calculation(5.0, 3.0, "add", 8.0)
        repr_str = repr(calc)
        assert "Calculation" in repr_str
        assert "5.0" in repr_str
        assert "add" in repr_str


class TestHistoryExtended:
    """Extended tests for calculation history."""
    
    def test_history_with_pandas_unavailable(self):
        """Test history functionality when pandas is unavailable."""
        with patch.dict('sys.modules', {'pandas': None}):
            config = CalculatorConfig()
            history = CalculationHistory(config)
            
            # Add calculation
            calc = Calculation(5.0, 3.0, "add", 8.0)
            history.add_calculation(calc)
            
            assert len(history.get_history()) == 1
    
    def test_history_save_load_errors(self):
        """Test history save/load error handling."""
        config = CalculatorConfig()
        history = CalculationHistory(config)
        
        # Test loading non-existent file
        result = history.load_from_csv("nonexistent.csv")
        assert result == False
        
        # Test saving to invalid location
        invalid_path = "/invalid/path/test.csv"
        result = history.save_to_csv(invalid_path)
        assert result == False
    
    def test_history_max_size_limit(self):
        """Test history size limitation."""
        config = CalculatorConfig()
        config.max_history_size = 3
        history = CalculationHistory(config)
        
        # Add more calculations than limit
        for i in range(5):
            calc = Calculation(float(i), 1.0, "add", float(i + 1))
            history.add_calculation(calc)
        
        # Should only keep last 3
        assert len(history.get_history()) == 3


class TestConfigurationExtended:
    """Extended configuration tests."""
    
    def test_config_property_getters(self):
        """Test configuration property getters."""
        config = CalculatorConfig()
        
        # Test all properties exist and have reasonable defaults
        assert hasattr(config, 'log_file')
        assert hasattr(config, 'history_file')
        assert config.max_history_size > 0
        assert config.precision >= 0
        assert config.max_input_value > 0
    
    def test_config_boolean_parsing(self):
        """Test boolean environment variable parsing."""
        import os
        
        # Save original value
        original = os.environ.get('CALCULATOR_AUTO_SAVE')
        
        try:
            # Test different boolean representations
            for value in ['true', 'True', 'TRUE', '1', 'yes']:
                os.environ['CALCULATOR_AUTO_SAVE'] = value
                config = CalculatorConfig()
                assert config.auto_save == True
                
            for value in ['false', 'False', 'FALSE', '0', 'no']:
                os.environ['CALCULATOR_AUTO_SAVE'] = value
                config = CalculatorConfig()
                assert config.auto_save == False
                
        finally:
            # Restore original value
            if original is not None:
                os.environ['CALCULATOR_AUTO_SAVE'] = original
            else:
                os.environ.pop('CALCULATOR_AUTO_SAVE', None)


class TestErrorHandlingExtended:
    """Extended error handling tests."""
    
    def test_operation_error_details(self):
        """Test operation error with details."""
        error = OperationError("divide", "Division by zero", 10.0, 0.0)
        assert "divide" in str(error)
        assert "Division by zero" in str(error)
    
    def test_validation_error_details(self):
        """Test validation error with details."""
        error = ValidationError("abc", "Not a number")
        assert "abc" in str(error)
        assert "Not a number" in str(error)
    
    def test_configuration_error(self):
        """Test configuration error."""
        error = ConfigurationError("Invalid setting")
        assert "Invalid setting" in str(error)


class TestMiscellaneousCoverage:
    """Tests for miscellaneous coverage improvements."""
    
    def test_operation_edge_cases(self):
        """Test operation edge cases."""
        from app.operations import calculate
        
        # Test very small numbers
        result = calculate("add", 0.000001, 0.000002)
        assert abs(result - 0.000003) < 1e-10
        
        # Test negative numbers
        result = calculate("multiply", -5.0, -3.0)
        assert result == 15.0
    
    def test_input_validator_edge_cases(self):
        """Test input validator edge cases."""
        from app.input_validators import InputValidator
        
        validator = InputValidator()
        
        # Test scientific notation
        result = validator.validate_number("1.5e2")
        assert result == 150.0
        
        # Test negative scientific notation
        result = validator.validate_number("-2.5e-1")
        assert result == -0.25
    
    def test_help_system_section_management(self):
        """Test help system section management."""
        from app.help_decorators import HelpMenuDecorator, HelpSection
        
        class TestHelpSection(HelpSection):
            def generate_content(self) -> str:
                return "Test content"
            
            def get_section_name(self) -> str:
                return "test"
        
        decorator = HelpMenuDecorator()
        test_section = TestHelpSection()
        
        # Test registration and unregistration
        decorator.register_section(test_section)
        assert "test" in decorator.get_available_sections()
        
        decorator.unregister_section("test")
        assert "test" not in decorator.get_available_sections()
    
    def test_observer_error_handling(self):
        """Test observer error handling."""
        from app.observers import Subject, Observer
        from app.calculation import Calculation
        
        class FailingObserver(Observer):
            def update(self, calculation):
                raise Exception("Test error")
            
            def get_observer_name(self):
                return "FailingObserver"
        
        subject = Subject()
        failing_observer = FailingObserver()
        subject.attach(failing_observer)
        
        # Should not raise exception even though observer fails
        calc = Calculation(1.0, 2.0, "add", 3.0)
        subject.notify(calc)  # Should handle exception gracefully
        
        assert subject.get_observer_count() == 1
