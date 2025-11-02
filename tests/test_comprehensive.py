"""Test cases for REPL interface and additional components."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys
from app.repl import CalculatorREPL
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.logger import CalculatorLogger
from app.observers import LoggingObserver, AutoSaveObserver
from app.help_decorators import HelpMenuDecorator, ExampleDecorator, CommandDecorator
from app.input_validators import InputValidator
from app.exceptions import ValidationError


class TestREPL:
    """Test REPL interface functionality."""
    
    def test_repl_initialization(self):
        """Test REPL initialization."""
        config = CalculatorConfig()
        repl = CalculatorREPL(config)
        assert repl.calculator is not None
        assert repl.config == config
    
    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_exit_command(self, mock_stdout, mock_input):
        """Test REPL exit command."""
        config = CalculatorConfig()
        repl = CalculatorREPL(config)
        repl.run()
        output = mock_stdout.getvalue()
        assert "Goodbye!" in output or "Thank you" in output
    
    @patch('builtins.input', side_effect=['help', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_help_command(self, mock_stdout, mock_input):
        """Test REPL help command."""
        config = CalculatorConfig()
        repl = CalculatorREPL(config)
        repl.run()
        output = mock_stdout.getvalue()
        assert "help" in output.lower() or "commands" in output.lower()
    
    @patch('builtins.input', side_effect=['add 5 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_calculation(self, mock_stdout, mock_input):
        """Test REPL calculation command."""
        config = CalculatorConfig()
        repl = CalculatorREPL(config)
        repl.run()
        output = mock_stdout.getvalue()
        assert "8" in output or "result" in output.lower()
    
    @patch('builtins.input', side_effect=['invalid command', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_invalid_command(self, mock_stdout, mock_input):
        """Test REPL invalid command handling."""
        config = CalculatorConfig()
        repl = CalculatorREPL(config)
        repl.run()
        output = mock_stdout.getvalue()
        assert "error" in output.lower() or "invalid" in output.lower() or "unknown" in output.lower()


class TestLogger:
    """Test logging functionality."""
    
    def test_logger_initialization(self):
        """Test logger initialization."""
        config = CalculatorConfig()
        logger = CalculatorLogger(config)
        assert logger.config == config
        assert logger.logger is not None
    
    def test_logger_log_methods(self):
        """Test logger logging methods."""
        config = CalculatorConfig()
        logger = CalculatorLogger(config)
        
        # Test different log levels
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        logger.debug("Test debug message")
        
        # Should not raise exceptions
        assert True


class TestObservers:
    """Test observer pattern implementation."""
    
    def test_logging_observer(self):
        """Test logging observer."""
        config = CalculatorConfig()
        logger = CalculatorLogger(config)
        observer = LoggingObserver(logger)
        
        # Test update method
        observer.update("Test calculation event")
        # Should not raise exceptions
        assert True
    
    def test_auto_save_observer(self):
        """Test auto-save observer."""
        config = CalculatorConfig()
        calculator = Calculator(config)
        observer = AutoSaveObserver(calculator)
        
        # Test update method
        observer.update("Test calculation event")
        # Should not raise exceptions
        assert True


class TestHelpDecorators:
    """Test help system decorators."""
    
    def test_help_menu_decorator(self):
        """Test basic help menu decorator."""
        decorator = HelpMenuDecorator()
        help_text = decorator.generate_full_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0
    
    def test_example_decorator(self):
        """Test example decorator."""
        base_decorator = HelpMenuDecorator()
        decorator = ExampleDecorator(base_decorator)
        help_text = decorator.generate_full_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0
    
    def test_command_decorator(self):
        """Test command decorator."""
        base_decorator = HelpMenuDecorator()
        decorator = CommandDecorator(base_decorator)
        help_text = decorator.generate_full_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0


class TestInputValidator:
    """Test input validation functionality."""
    
    def test_validate_number_valid(self):
        """Test valid number validation."""
        config = CalculatorConfig()
        validator = InputValidator(config)
        
        result = validator.validate_number("123.45")
        assert result == 123.45
        
        result = validator.validate_number("-67.89")
        assert result == -67.89
    
    def test_validate_number_invalid(self):
        """Test invalid number validation."""
        config = CalculatorConfig()
        validator = InputValidator(config)
        
        with pytest.raises(ValidationError):
            validator.validate_number("not_a_number")
        
        with pytest.raises(ValidationError):
            validator.validate_number("")
    
    def test_validate_number_range(self):
        """Test number range validation."""
        config = CalculatorConfig()
        config.max_input_value = 100.0
        validator = InputValidator(config)
        
        # Valid range
        result = validator.validate_number("50.0")
        assert result == 50.0
        
        # Invalid range
        with pytest.raises(ValidationError):
            validator.validate_number("150.0")
    
    def test_validate_operation_valid(self):
        """Test valid operation validation."""
        config = CalculatorConfig()
        validator = InputValidator(config)
        
        assert validator.validate_operation("add") == "add"
        assert validator.validate_operation("multiply") == "multiply"
    
    def test_validate_operation_invalid(self):
        """Test invalid operation validation."""
        config = CalculatorConfig()
        validator = InputValidator(config)
        
        with pytest.raises(ValidationError):
            validator.validate_operation("invalid_op")
        
        with pytest.raises(ValidationError):
            validator.validate_operation("")


class TestConfigurationEdgeCases:
    """Test configuration edge cases."""
    
    def test_config_with_environment_variables(self):
        """Test configuration with environment variables."""
        import os
        
        # Save original values
        original_values = {}
        env_vars = [
            'CALCULATOR_MAX_HISTORY_SIZE',
            'CALCULATOR_PRECISION',
            'CALCULATOR_MAX_INPUT_VALUE',
            'CALCULATOR_AUTO_SAVE'
        ]
        
        for var in env_vars:
            original_values[var] = os.environ.get(var)
        
        try:
            # Set test values
            os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '50'
            os.environ['CALCULATOR_PRECISION'] = '3'
            os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '500000'
            os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
            
            config = CalculatorConfig()
            assert config.max_history_size == 50
            assert config.precision == 3
            assert config.max_input_value == 500000.0
            assert config.auto_save == False
            
        finally:
            # Restore original values
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value
                else:
                    os.environ.pop(var, None)
    
    def test_config_directory_creation(self):
        """Test configuration directory creation."""
        config = CalculatorConfig()
        
        # Directories should be Path objects
        assert hasattr(config.log_dir, 'mkdir')
        assert hasattr(config.history_dir, 'mkdir')


class TestCalculatorIntegration:
    """Test calculator integration scenarios."""
    
    def test_calculator_with_observers(self):
        """Test calculator with all observers attached."""
        config = CalculatorConfig()
        calculator = Calculator(config)
        
        # Add observers
        logger = CalculatorLogger(config)
        log_observer = LoggingObserver(logger)
        auto_save_observer = AutoSaveObserver(calculator)
        
        calculator.attach_observer(log_observer)
        calculator.attach_observer(auto_save_observer)
        
        # Perform calculation
        result = calculator.perform_calculation("add", "5", "3")
        assert result.result == 8.0
        
        # Test undo/redo
        calculator.undo_last_calculation()
        assert len(calculator.get_history()) == 0
        
        calculator.redo_last_calculation()
        assert len(calculator.get_history()) == 1
    
    def test_calculator_error_handling(self):
        """Test calculator error handling."""
        config = CalculatorConfig()
        calculator = Calculator(config)
        
        with pytest.raises(Exception):  # Should raise an appropriate exception
            calculator.perform_calculation("divide", "5", "0")
    
    def test_calculator_history_management(self):
        """Test calculator history management."""
        config = CalculatorConfig()
        calculator = Calculator(config)
        
        # Add multiple calculations
        calculator.perform_calculation("add", "1", "2")
        calculator.perform_calculation("multiply", "3", "4")
        calculator.perform_calculation("subtract", "10", "5")
        
        history = calculator.get_history()
        assert len(history) == 3
        
        # Clear history
        calculator.clear_history()
        assert len(calculator.get_history()) == 0


class TestUtilityFunctions:
    """Test utility functions and edge cases."""
    
    def test_calculation_string_representation(self):
        """Test calculation string representation."""
        from app.calculation import Calculation
        calc = Calculation(5.0, 3.0, "add", 8.0)
        str_repr = str(calc)
        assert "5.0" in str_repr
        assert "3.0" in str_repr
        assert "add" in str_repr
        assert "8.0" in str_repr
    
    def test_calculation_equality(self):
        """Test calculation equality."""
        from app.calculation import Calculation
        calc1 = Calculation(5.0, 3.0, "add", 8.0)
        calc2 = Calculation(5.0, 3.0, "add", 8.0)
        calc3 = Calculation(5.0, 3.0, "multiply", 15.0)
        
        assert calc1 == calc2
        assert calc1 != calc3
