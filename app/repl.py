"""Command-Line Interface (REPL) for the calculator application."""

import sys
from typing import List, Optional, Dict, Any
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError, OperationError, ValidationError
from app.help_decorators import HelpMenuDecorator, DynamicHelpMixin


class CalculatorREPL:
    """Read-Eval-Print Loop interface for the calculator."""
    
    def __init__(self):
        """Initialize REPL with calculator instance."""
        try:
            self.config = CalculatorConfig()
            self.calculator = Calculator(self.config)
            self.running = True
            self.help_generator = HelpMenuDecorator()
            
            # Welcome message
            print("🧮 Advanced Calculator Application")
            print("Type 'help' for available commands or 'exit' to quit.\n")
            
        except Exception as e:
            print(f"Error initializing calculator: {e}")
            sys.exit(1)
    
    def run(self) -> None:
        """Start the REPL loop."""
        while self.running:
            try:
                user_input = input("calculator> ").strip()
                
                if not user_input:
                    continue
                
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
    
    def _process_command(self, command: str) -> None:
        """Process user command."""
        parts = command.split()
        
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        # Basic commands
        if cmd == "exit" or cmd == "quit":
            self._handle_exit()
        elif cmd == "help":
            self._show_help(parts[1:])
        elif cmd == "history":
            self._show_history()
        elif cmd == "clear":
            self._clear_history()
        elif cmd == "undo":
            self._handle_undo()
        elif cmd == "redo":
            self._handle_redo()
        elif cmd == "save":
            self._handle_save(parts[1:])
        elif cmd == "load":
            self._handle_load(parts[1:])
        elif cmd == "info":
            self._show_calculator_info()
        elif cmd in self.calculator.get_available_operations():
            self._handle_calculation(cmd, parts[1:])
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
    
    def _handle_calculation(self, operation: str, args: List[str]) -> None:
        """Handle calculation commands."""
        if len(args) != 2:
            print(f"Usage: {operation} <number1> <number2>")
            return
        
        try:
            result = self.calculator.perform_calculation(operation, args[0], args[1])
            print(f"Result: {result}")
            
        except (OperationError, ValidationError, CalculatorError) as e:
            print(f"Error: {e}")
    
    def _show_help(self, args: List[str]) -> None:
        """Display help information using dynamic help decorator."""
        if args and len(args) > 0:
            # Show help for specific section
            section_name = args[0].lower()
            try:
                help_text = self.help_generator.generate_section_help(section_name)
                print(help_text)
            except Exception:
                print(f"❌ Unknown help section: {section_name}")
                print("Available sections: operations, history, file, system")
        else:
            # Show general help using dynamic decorator pattern
            try:
                help_text = self.help_generator.generate_full_help()
                print(help_text)
            except Exception as e:
                # Fallback to basic help if decorator fails
                print("📖 Basic Calculator Help")
                print("Available operations:", ", ".join(self.calculator.get_available_operations()))
                print("Type: <operation> <num1> <num2>")
                print("Commands: history, clear, undo, redo, save, load, info, exit")
    
    def _show_history(self) -> None:
        """Display calculation history."""
        history = self.calculator.get_history()
        
        if not history:
            print("No calculations in history.")
            return
        
        print("\n📜 Calculation History:")
        for i, calc in enumerate(history, 1):
            print(f"  {i}. {calc}")
        
        summary = self.calculator.get_history_summary()
        print(f"\nTotal calculations: {summary['total_calculations']}")
        print(f"Undo available: {summary['undo_available']} ({summary.get('undo_count', 0)} states)")
        print(f"Redo available: {summary['redo_available']} ({summary.get('redo_count', 0)} states)")
        print()
    
    def _clear_history(self) -> None:
        """Clear calculation history."""
        self.calculator.clear_history()
        print("✅ History cleared.")
    
    def _handle_undo(self) -> None:
        """Handle undo command."""
        if self.calculator.undo():
            print("✅ Last calculation undone.")
        else:
            print("❌ Nothing to undo.")
    
    def _handle_redo(self) -> None:
        """Handle redo command."""
        if self.calculator.redo():
            print("✅ Calculation redone.")
        else:
            print("❌ Nothing to redo.")
    
    def _handle_save(self, args: List[str]) -> None:
        """Handle save command."""
        try:
            filename = args[0] if args else None
            self.calculator.save_history(filename)
            print("✅ History saved successfully.")
        except Exception as e:
            print(f"❌ Error saving history: {e}")
    
    def _handle_load(self, args: List[str]) -> None:
        """Handle load command."""
        try:
            filename = args[0] if args else None
            self.calculator.load_history(filename)
            print("✅ History loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading history: {e}")
    
    def _show_calculator_info(self) -> None:
        """Display calculator information."""
        info = self.calculator.get_calculator_info()
        
        print("\n🔧 Calculator Information:")
        print(f"  Precision: {info['precision']} decimal places")
        print(f"  Max input value: {info['max_input_value']:,}")
        print(f"  Max history size: {info['max_history_size']}")
        print(f"  Auto-save enabled: {info['auto_save_enabled']}")
        print(f"  Current history count: {info['history_count']}")
        print(f"  Observers attached: {info['observers_attached']}")
        print(f"  Available operations: {len(info['available_operations'])}")
        print()
    
    def _handle_exit(self) -> None:
        """Handle exit command."""
        print("Goodbye! 👋")
        self.running = False


def main():
    """Main entry point for the calculator REPL."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":
    main()
