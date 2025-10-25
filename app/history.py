"""History management for calculator calculations."""

from typing import List, Optional, Iterator
import pandas as pd
from pathlib import Path
from app.calculation import Calculation
from app.calculator_memento import MementoManager
from app.exceptions import OperationError
from app.calculator_config import CalculatorConfig


class CalculationHistory:
    """Manages calculation history with persistence and memento support."""
    
    def __init__(self, config: CalculatorConfig):
        """Initialize history with configuration."""
        self.config = config
        self._calculations: List[Calculation] = []
        self._memento_manager = MementoManager(max_states=50)
        
        # Save initial empty state
        self._memento_manager.save_state(self._calculations)
    
    def add_calculation(self, calculation: Calculation) -> None:
        """Add a calculation to history."""
        self._calculations.append(calculation)
        
        # Enforce maximum history size
        if len(self._calculations) > self.config.max_history_size:
            self._calculations.pop(0)
        
        # Save state for undo/redo
        self._memento_manager.save_state(self._calculations)
    
    def get_all_calculations(self) -> List[Calculation]:
        """Get all calculations in history."""
        return self._calculations.copy()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """Get the most recent calculation."""
        return self._calculations[-1] if self._calculations else None
    
    def get_calculation_count(self) -> int:
        """Get total number of calculations."""
        return len(self._calculations)
    
    def clear_history(self) -> None:
        """Clear all calculations from history."""
        self._calculations.clear()
        self._memento_manager.clear()
        self._memento_manager.save_state(self._calculations)
    
    def undo(self) -> bool:
        """Undo last calculation."""
        memento = self._memento_manager.undo()
        if memento:
            self._calculations = memento.get_history()
            return True
        return False
    
    def redo(self) -> bool:
        """Redo last undone calculation."""
        memento = self._memento_manager.redo()
        if memento:
            self._calculations = memento.get_history()
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._memento_manager.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._memento_manager.can_redo()
    
    def get_undo_count(self) -> int:
        """Get number of possible undo operations."""
        return self._memento_manager.get_undo_count()
    
    def get_redo_count(self) -> int:
        """Get number of possible redo operations."""
        return self._memento_manager.get_redo_count()
    
    def save_to_csv(self, file_path: Optional[Path] = None) -> None:
        """Save history to CSV file using pandas."""
        if file_path is None:
            file_path = self.config.history_file
        
        if not self._calculations:
            # Create empty CSV if no calculations
            empty_df = pd.DataFrame(columns=['operand1', 'operand2', 'operation', 'result', 'timestamp'])
            empty_df.to_csv(file_path, index=False, encoding=self.config.default_encoding)
            return
        
        try:
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._calculations]
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            df.to_csv(file_path, index=False, encoding=self.config.default_encoding)
            
        except Exception as e:
            raise OperationError("save_history", f"Failed to save history to CSV: {str(e)}")
    
    def load_from_csv(self, file_path: Optional[Path] = None) -> None:
        """Load history from CSV file using pandas."""
        if file_path is None:
            file_path = self.config.history_file
        
        if not file_path.exists():
            # File doesn't exist, start with empty history
            self._calculations.clear()
            self._memento_manager.clear()
            self._memento_manager.save_state(self._calculations)
            return
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path, encoding=self.config.default_encoding)
            
            # Clear current history
            self._calculations.clear()
            
            # Convert DataFrame rows to Calculation objects
            for _, row in df.iterrows():
                calc = Calculation.from_dict(row.to_dict())
                self._calculations.append(calc)
            
            # Reset memento manager and save current state
            self._memento_manager.clear()
            self._memento_manager.save_state(self._calculations)
            
        except Exception as e:
            raise OperationError("load_history", f"Failed to load history from CSV: {str(e)}")
    
    def get_history_summary(self) -> dict:
        """Get summary statistics of calculation history."""
        if not self._calculations:
            return {
                "total_calculations": 0,
                "operations_used": [],
                "most_recent": None,
                "undo_available": False,
                "redo_available": False
            }
        
        operations_used = list(set(calc.operation for calc in self._calculations))
        most_recent = self._calculations[-1]
        
        return {
            "total_calculations": len(self._calculations),
            "operations_used": operations_used,
            "most_recent": str(most_recent),
            "undo_available": self.can_undo(),
            "redo_available": self.can_redo(),
            "undo_count": self.get_undo_count(),
            "redo_count": self.get_redo_count()
        }
    
    def __len__(self) -> int:
        """Return number of calculations in history."""
        return len(self._calculations)
    
    def __iter__(self) -> Iterator[Calculation]:
        """Make history iterable."""
        return iter(self._calculations)
    
    def __getitem__(self, index: int) -> Calculation:
        """Get calculation by index."""
        return self._calculations[index]
