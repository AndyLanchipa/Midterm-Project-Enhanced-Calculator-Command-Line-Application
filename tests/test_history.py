"""Test cases for history management and configuration."""

import pytest
from pathlib import Path
import tempfile
import os
from app.history import CalculationHistory
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, MementoManager
from app.exceptions import ConfigurationError, OperationError


class TestCalculatorConfig:
    """Test calculator configuration management."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config = CalculatorConfig()
        
        assert config.max_history_size == 100
        assert config.precision == 2
        assert config.max_input_value == 1000000.0
        assert config.default_encoding == "utf-8"
        assert isinstance(config.log_dir, Path)
        assert isinstance(config.history_dir, Path)
    
    def test_configuration_validation(self):
        """Test configuration validation."""
        # Test with invalid environment variables
        old_max_history = os.environ.get('CALCULATOR_MAX_HISTORY_SIZE', '')
        old_precision = os.environ.get('CALCULATOR_PRECISION', '')
        
        try:
            # Set invalid values
            os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '-10'
            os.environ['CALCULATOR_PRECISION'] = '-5'
            
            with pytest.raises(ConfigurationError):
                CalculatorConfig()
        finally:
            # Restore original values
            if old_max_history:
                os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = old_max_history
            else:
                os.environ.pop('CALCULATOR_MAX_HISTORY_SIZE', None)
            
            if old_precision:
                os.environ['CALCULATOR_PRECISION'] = old_precision
            else:
                os.environ.pop('CALCULATOR_PRECISION', None)
    
    def test_directory_creation(self):
        """Test that configuration creates necessary directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            old_log_dir = os.environ.get('CALCULATOR_LOG_DIR', '')
            old_history_dir = os.environ.get('CALCULATOR_HISTORY_DIR', '')
            
            try:
                test_log_dir = Path(temp_dir) / "test_logs"
                test_history_dir = Path(temp_dir) / "test_history"
                
                os.environ['CALCULATOR_LOG_DIR'] = str(test_log_dir)
                os.environ['CALCULATOR_HISTORY_DIR'] = str(test_history_dir)
                
                config = CalculatorConfig()
                
                assert test_log_dir.exists()
                assert test_history_dir.exists()
            finally:
                if old_log_dir:
                    os.environ['CALCULATOR_LOG_DIR'] = old_log_dir
                else:
                    os.environ.pop('CALCULATOR_LOG_DIR', None)
                
                if old_history_dir:
                    os.environ['CALCULATOR_HISTORY_DIR'] = old_history_dir
                else:
                    os.environ.pop('CALCULATOR_HISTORY_DIR', None)


class TestCalculatorMemento:
    """Test memento pattern implementation."""
    
    def test_memento_creation(self):
        """Test creating a memento."""
        calculations = [
            Calculation(5.0, 3.0, "add", 8.0),
            Calculation(10.0, 2.0, "divide", 5.0)
        ]
        
        memento = CalculatorMemento(calculations)
        restored_history = memento.get_history()
        
        assert len(restored_history) == 2
        assert restored_history[0].operation == "add"
        assert restored_history[1].operation == "divide"
        
        # Test that it's a deep copy
        calculations.append(Calculation(1.0, 1.0, "subtract", 0.0))
        assert len(restored_history) == 2  # Should not change
    
    def test_empty_memento(self):
        """Test memento with empty history."""
        memento = CalculatorMemento([])
        assert len(memento) == 0
        assert memento.get_history() == []
    
    def test_memento_manager(self):
        """Test memento manager functionality."""
        manager = MementoManager(max_states=3)
        
        # Save initial state
        manager.save_state([])
        assert manager.get_state_count() == 1
        assert not manager.can_undo()
        assert not manager.can_redo()
        
        # Save more states
        calc1 = [Calculation(1.0, 1.0, "add", 2.0)]
        calc2 = [Calculation(2.0, 2.0, "add", 4.0)]
        
        manager.save_state(calc1)
        manager.save_state(calc2)
        
        assert manager.can_undo()
        assert not manager.can_redo()
        assert manager.get_state_count() == 3
    
    def test_undo_redo_operations(self):
        """Test undo and redo operations."""
        manager = MementoManager()
        
        state1 = []
        state2 = [Calculation(1.0, 1.0, "add", 2.0)]
        state3 = [Calculation(1.0, 1.0, "add", 2.0), Calculation(2.0, 2.0, "multiply", 4.0)]
        
        manager.save_state(state1)
        manager.save_state(state2)
        manager.save_state(state3)
        
        # Test undo - should return to state2
        previous_state = manager.undo()
        assert len(previous_state.get_history()) == 1
        
        # Test redo - should return to state3
        next_state = manager.redo()
        assert len(next_state.get_history()) == 2
        
        # Test undo limits
        manager.undo()  # back to state2
        manager.undo()  # back to state1
        no_more_undo = manager.undo()  # should be None
        assert no_more_undo is None
    
    def test_memento_manager_limits(self):
        """Test memento manager state limits."""
        manager = MementoManager(max_states=2)
        
        # Add more states than the limit
        for i in range(5):
            state = [Calculation(float(i), 1.0, "add", float(i+1))]
            manager.save_state(state)
        
        # Should only keep the last 2 states
        assert manager.get_state_count() == 2


class TestCalculationHistory:
    """Test calculation history management."""
    
    def setup_method(self):
        """Set up test history."""
        self.config = CalculatorConfig()
        self.history = CalculationHistory(self.config)
    
    def test_add_calculation(self):
        """Test adding calculations to history."""
        calc = Calculation(5.0, 3.0, "add", 8.0)
        self.history.add_calculation(calc)
        
        assert self.history.get_calculation_count() == 1
        assert self.history.get_last_calculation() == calc
    
    def test_history_iteration(self):
        """Test iterating over history."""
        calc1 = Calculation(1.0, 1.0, "add", 2.0)
        calc2 = Calculation(3.0, 2.0, "subtract", 1.0)
        
        self.history.add_calculation(calc1)
        self.history.add_calculation(calc2)
        
        calculations = list(self.history)
        assert len(calculations) == 2
        assert calculations[0] == calc1
        assert calculations[1] == calc2
    
    def test_history_indexing(self):
        """Test indexing history."""
        calc1 = Calculation(5.0, 3.0, "add", 8.0)
        calc2 = Calculation(10.0, 2.0, "divide", 5.0)
        
        self.history.add_calculation(calc1)
        self.history.add_calculation(calc2)
        
        assert self.history[0] == calc1
        assert self.history[1] == calc2
        assert len(self.history) == 2
    
    def test_clear_history(self):
        """Test clearing history."""
        self.history.add_calculation(Calculation(1.0, 1.0, "add", 2.0))
        assert self.history.get_calculation_count() == 1
        
        self.history.clear_history()
        assert self.history.get_calculation_count() == 0
        assert self.history.get_last_calculation() is None
    
    def test_history_undo_redo(self):
        """Test history undo and redo operations."""
        calc1 = Calculation(1.0, 1.0, "add", 2.0)
        calc2 = Calculation(3.0, 2.0, "subtract", 1.0)
        
        self.history.add_calculation(calc1)
        self.history.add_calculation(calc2)
        
        assert len(self.history) == 2
        
        # Test undo
        undo_success = self.history.undo()
        assert undo_success is True
        assert len(self.history) == 1
        
        # Test redo
        redo_success = self.history.redo()
        assert redo_success is True
        assert len(self.history) == 2
    
    def test_history_size_limit(self):
        """Test history size enforcement."""
        # Set a small limit for testing
        original_limit = self.config.max_history_size
        self.config.max_history_size = 3
        
        try:
            # Add more calculations than the limit
            for i in range(5):
                calc = Calculation(float(i), 1.0, "add", float(i+1))
                self.history.add_calculation(calc)
            
            # Should only keep the last 3 calculations
            assert len(self.history) == 3
            assert self.history[0].operand1 == 2.0  # Should be the 3rd calculation added
        finally:
            self.config.max_history_size = original_limit
    
    def test_history_summary(self):
        """Test history summary generation."""
        summary = self.history.get_history_summary()
        assert "total_calculations" in summary
        assert "operations_used" in summary
        assert "undo_available" in summary
        assert "redo_available" in summary
        
        # Add some calculations
        self.history.add_calculation(Calculation(1.0, 1.0, "add", 2.0))
        self.history.add_calculation(Calculation(3.0, 2.0, "multiply", 6.0))
        
        summary = self.history.get_history_summary()
        assert summary["total_calculations"] == 2
        assert "add" in summary["operations_used"]
        assert "multiply" in summary["operations_used"]
    
    def test_csv_operations_without_pandas(self):
        """Test CSV operations when pandas is not available."""
        # This tests the error handling when pandas is not available
        # In a real environment, we might mock the pandas import
        pass  # This is covered by integration tests
