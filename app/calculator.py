"""Main calculator class integrating all design patterns and functionality."""

from typing import Optional, List, Dict, Any
from app.calculation import Calculation
from app.operations import OperationFactory, calculate
from app.history import CalculationHistory
from app.calculator_config import CalculatorConfig
from app.logger import CalculatorLogger
from app.input_validators import InputValidator
from app.observers import Subject, LoggingObserver, AutoSaveObserver
from app.exceptions import CalculatorError, OperationError, ValidationError


class Calculator(Subject):
    """Main calculator class implementing all design patterns and functionality."""
    
    def __init__(self, config: Optional[CalculatorConfig] = None):
        """Initialize calculator with configuration."""
        super().__init__()
        
        # Initialize configuration
        self.config = config or CalculatorConfig()
        
        # Initialize components
        self.logger = CalculatorLogger(self.config)
        self.history = CalculationHistory(self.config)
        self.validator = InputValidator(
            max_value=self.config.max_input_value,
            precision=self.config.precision
        )
        
        # Set up observers if auto-save is enabled
        self._setup_observers()
        
        # Log calculator initialization
        self.logger.log_system_event("Calculator initialized", 
                                     f"Max history: {self.config.max_history_size}")
    
    def _setup_observers(self) -> None:
        """Set up observers based on configuration."""
        # Always attach logging observer
        logging_observer = LoggingObserver(self.logger)
        self.attach(logging_observer)
        
        # Attach auto-save observer if enabled
        if self.config.auto_save:
            autosave_observer = AutoSaveObserver(self.history)
            self.attach(autosave_observer)
            self.logger.log_config_action("Auto-save enabled")
    
    def perform_calculation(self, operation_name: str, operand1_str: str, operand2_str: str) -> Calculation:
        """Perform a calculation with string inputs."""
        try:
            # Validate operation
            if not OperationFactory.get_available_operations().__contains__(operation_name.lower()):
                available = ", ".join(OperationFactory.get_available_operations())
                raise OperationError(operation_name, f"Available operations: {available}")
            
            # Validate and convert inputs
            if operation_name.lower() == "divide":
                operand1, operand2 = self.validator.validate_division(operand1_str, operand2_str)
            elif operation_name.lower() == "root":
                operand1, operand2 = self.validator.validate_root(operand1_str, operand2_str)
            elif operation_name.lower() == "power":
                operand1, operand2 = self.validator.validate_power(operand1_str, operand2_str)
            else:
                operand1, operand2 = self.validator.validate_operation_inputs(operand1_str, operand2_str)
            
            # Perform calculation
            result = calculate(operation_name, operand1, operand2)
            
            # Format result according to precision
            formatted_result = float(self.validator.format_result(result))
            
            # Create calculation object
            calculation = Calculation(operand1, operand2, operation_name.lower(), formatted_result)
            
            # Add to history
            self.history.add_calculation(calculation)
            
            # Notify observers
            self.notify(calculation)
            
            return calculation
            
        except (OperationError, ValidationError) as e:
            self.logger.log_error(operation_name, str(e), 
                                operand1=None if 'operand1' not in locals() else operand1,
                                operand2=None if 'operand2' not in locals() else operand2)
            raise
        except Exception as e:
            self.logger.log_error(operation_name, f"Unexpected error: {str(e)}")
            raise CalculatorError(f"Calculation failed: {str(e)}")
    
    def get_history(self) -> List[Calculation]:
        """Get calculation history."""
        return self.history.get_all_calculations()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """Get the last calculation."""
        return self.history.get_last_calculation()
    
    def clear_history(self) -> None:
        """Clear calculation history."""
        self.history.clear_history()
        self.logger.log_history_action("History cleared")
    
    def undo(self) -> bool:
        """Undo last calculation."""
        if self.history.undo():
            self.logger.log_history_action("Undo performed")
            return True
        return False
    
    def redo(self) -> bool:
        """Redo last undone calculation."""
        if self.history.redo():
            self.logger.log_history_action("Redo performed")
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.history.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.history.can_redo()
    
    def save_history(self, file_path: Optional[str] = None) -> None:
        """Manually save history to file."""
        try:
            if file_path:
                from pathlib import Path
                self.history.save_to_csv(Path(file_path))
            else:
                self.history.save_to_csv()
            self.logger.log_history_action("History saved manually")
        except Exception as e:
            self.logger.log_error("save_history", str(e))
            raise
    
    def load_history(self, file_path: Optional[str] = None) -> None:
        """Load history from file."""
        try:
            if file_path:
                from pathlib import Path
                self.history.load_from_csv(Path(file_path))
            else:
                self.history.load_from_csv()
            self.logger.log_history_action("History loaded")
        except Exception as e:
            self.logger.log_error("load_history", str(e))
            raise
    
    def get_available_operations(self) -> List[str]:
        """Get list of available operations."""
        return OperationFactory.get_available_operations()
    
    def get_history_summary(self) -> Dict[str, Any]:
        """Get summary of calculation history."""
        return self.history.get_history_summary()
    
    def get_calculator_info(self) -> Dict[str, Any]:
        """Get calculator configuration and status information."""
        return {
            "precision": self.config.precision,
            "max_input_value": self.config.max_input_value,
            "max_history_size": self.config.max_history_size,
            "auto_save_enabled": self.config.auto_save,
            "history_count": len(self.history),
            "undo_available": self.can_undo(),
            "redo_available": self.can_redo(),
            "observers_attached": self.get_observer_count(),
            "available_operations": self.get_available_operations()
        }
