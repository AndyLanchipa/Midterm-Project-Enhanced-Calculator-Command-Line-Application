"""Memento pattern implementation for calculator state management."""

from typing import List, Optional
from copy import deepcopy
from app.calculation import Calculation


class CalculatorMemento:
    """Memento class to store calculator state for undo/redo functionality."""
    
    def __init__(self, history: List[Calculation]):
        """Initialize memento with current calculator state."""
        self._history = deepcopy(history)
        self._timestamp = None
        if history:
            self._timestamp = history[-1].timestamp
    
    def get_history(self) -> List[Calculation]:
        """Get the stored history state."""
        return deepcopy(self._history)
    
    def get_timestamp(self):
        """Get the timestamp when this memento was created."""
        return self._timestamp
    
    def __len__(self) -> int:
        """Return the number of calculations in this memento."""
        return len(self._history)
    
    def __str__(self) -> str:
        """String representation of memento."""
        if not self._history:
            return "Empty calculator state"
        return f"Calculator state with {len(self._history)} calculations"


class MementoManager:
    """Manages memento objects for undo/redo functionality."""
    
    def __init__(self, max_states: int = 50):
        """Initialize memento manager with maximum number of states."""
        self._max_states = max_states
        self._mementos: List[CalculatorMemento] = []
        self._current_index = -1
    
    def save_state(self, history: List[Calculation]) -> None:
        """Save current calculator state as a memento."""
        # Remove any mementos after current index (when undoing then making new calculations)
        if self._current_index < len(self._mementos) - 1:
            self._mementos = self._mementos[:self._current_index + 1]
        
        # Create new memento
        memento = CalculatorMemento(history)
        self._mementos.append(memento)
        self._current_index += 1
        
        # Remove oldest mementos if we exceed max states
        if len(self._mementos) > self._max_states:
            self._mementos.pop(0)
            self._current_index -= 1
    
    def undo(self) -> Optional[CalculatorMemento]:
        """Undo to previous state."""
        if self.can_undo():
            self._current_index -= 1
            return self._mementos[self._current_index]
        return None
    
    def redo(self) -> Optional[CalculatorMemento]:
        """Redo to next state."""
        if self.can_redo():
            self._current_index += 1
            return self._mementos[self._current_index]
        return None
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._mementos) - 1
    
    def get_current_state(self) -> Optional[CalculatorMemento]:
        """Get current memento state."""
        if 0 <= self._current_index < len(self._mementos):
            return self._mementos[self._current_index]
        return None
    
    def clear(self) -> None:
        """Clear all mementos."""
        self._mementos.clear()
        self._current_index = -1
    
    def get_state_count(self) -> int:
        """Get number of saved states."""
        return len(self._mementos)
    
    def get_undo_count(self) -> int:
        """Get number of possible undo operations."""
        return max(0, self._current_index)
    
    def get_redo_count(self) -> int:
        """Get number of possible redo operations."""
        return max(0, len(self._mementos) - self._current_index - 1)
