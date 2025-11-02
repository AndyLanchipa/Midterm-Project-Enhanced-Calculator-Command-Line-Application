# Advanced Calculator Command-Line Application

A sophisticated Python calculator application featuring advanced operations, history management, and extensible architecture using multiple design patterns.

## Features

### Core Functionality
- **10 Arithmetic Operations**: Addition, Subtraction, Multiplication, Division, Power, Root, Modulus, Integer Division, Percentage, and Absolute Difference
- **Interactive REPL Interface**: Command-line interface with comprehensive help system
- **History Management**: Full calculation history with undo/redo functionality
- **Data Persistence**: Save/load calculation history to CSV files using pandas
- **Input Validation**: Robust validation with meaningful error messages
- **Configurable Settings**: Environment-based configuration management

### Design Patterns Implemented
- **Factory Pattern**: Dynamic operation creation and management
- **Memento Pattern**: Undo/redo functionality with state management
- **Observer Pattern**: Automatic logging and auto-save capabilities
- **Decorator Pattern**: Dynamic help menu generation (Advanced Feature)

### Advanced Features
- **Dynamic Help System**: Context-aware help that automatically updates when new operations are added
- **Comprehensive Logging**: Multi-level logging with file rotation
- **Error Handling**: Custom exceptions with detailed error messages
- **Extensible Architecture**: Easy to add new operations and features

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/AndyLanchipa/Midterm-Project-Enhanced-Calculator-Command-Line-Application.git
cd Midterm-Project-Enhanced-Calculator-Command-Line-Application
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration (optional):
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Running the Application
```bash
python main.py
```

### Available Commands

#### Arithmetic Operations
- `add <num1> <num2>` - Add two numbers
- `subtract <num1> <num2>` - Subtract second from first
- `multiply <num1> <num2>` - Multiply two numbers
- `divide <num1> <num2>` - Divide first by second
- `power <base> <exponent>` - Raise base to exponent
- `root <number> <root>` - Calculate nth root of number
- `modulus <num1> <num2>` - Calculate remainder of division
- `int_divide <num1> <num2>` - Integer division (floor division)
- `percent <part> <whole>` - Calculate percentage
- `abs_diff <num1> <num2>` - Absolute difference between numbers

#### History Management
- `history` - Show calculation history
- `clear` - Clear calculation history
- `undo` - Undo last calculation
- `redo` - Redo last undone calculation

#### File Operations
- `save [filename]` - Save history to CSV file
- `load [filename]` - Load history from CSV file

#### Other Commands
- `help [section]` - Show help (general or section-specific)
- `info` - Show calculator information
- `exit` or `quit` - Exit the application

### Example Usage
```
calculator> add 5 3
Result: 5.0 add 3.0 = 8.0

calculator> power 2 8
Result: 2.0 power 8.0 = 256.0

calculator> history
Calculation History:
  1. 5.0 add 3.0 = 8.0
  2. 2.0 power 8.0 = 256.0

calculator> undo
Last calculation undone.

calculator> help operations
[Dynamic help for operations section]
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Directory Settings
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Configuration Options
- **CALCULATOR_LOG_DIR**: Directory for log files (default: logs)
- **CALCULATOR_HISTORY_DIR**: Directory for history files (default: history)
- **CALCULATOR_MAX_HISTORY_SIZE**: Maximum number of calculations to store (default: 100)
- **CALCULATOR_AUTO_SAVE**: Enable automatic saving to CSV (default: true)
- **CALCULATOR_PRECISION**: Decimal places for results (default: 2)
- **CALCULATOR_MAX_INPUT_VALUE**: Maximum allowed input value (default: 1000000)
- **CALCULATOR_DEFAULT_ENCODING**: File encoding (default: utf-8)

## Testing

### Running Tests
```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_operations.py -v
```

### Test Coverage
The project maintains 90%+ test coverage with comprehensive tests for:
- All arithmetic operations and edge cases
- Calculator core functionality
- History management and memento pattern
- Configuration and validation
- Error handling and exceptions
- Design pattern implementations

### Continuous Integration
GitHub Actions automatically runs tests on:
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)
- Push to main branch
- Pull requests
- Code linting and formatting checks
- Coverage enforcement

## Architecture

### Project Structure
```
project_root/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── calculator.py             # Main Calculator class
│   ├── calculation.py            # Calculation model
│   ├── calculator_config.py      # Configuration management
│   ├── calculator_memento.py     # Memento pattern implementation
│   ├── exceptions.py             # Custom exceptions
│   ├── help_decorators.py        # Dynamic help system (Decorator pattern)
│   ├── history.py                # History management
│   ├── input_validators.py       # Input validation
│   ├── logger.py                 # Logging system
│   ├── observers.py              # Observer pattern implementation
│   ├── operations.py             # Operations and Factory pattern
│   └── repl.py                   # REPL interface
├── tests/                        # Test suite
│   ├── test_calculator.py
│   ├── test_history.py
│   └── test_operations.py
├── .github/workflows/            # CI/CD pipeline
│   └── python-app.yml
├── logs/                         # Log files (created automatically)
├── history/                      # History files (created automatically)
├── .env                          # Configuration file
├── requirements.txt              # Python dependencies
├── main.py                       # Application entry point
└── README.md                     # This file
```

### Design Patterns

#### Factory Pattern
- **OperationFactory**: Creates operation instances dynamically
- **Benefits**: Easy to add new operations, centralized operation management
- **Implementation**: `app/operations.py`

#### Memento Pattern  
- **CalculatorMemento**: Stores calculator state for undo/redo
- **MementoManager**: Manages multiple states with configurable limits
- **Benefits**: Undo/redo functionality, state preservation
- **Implementation**: `app/calculator_memento.py`

#### Observer Pattern
- **LoggingObserver**: Automatically logs calculations
- **AutoSaveObserver**: Automatically saves history to CSV
- **Benefits**: Decoupled event handling, extensible notification system
- **Implementation**: `app/observers.py`

#### Decorator Pattern (Advanced Feature)
- **HelpMenuDecorator**: Dynamically generates context-aware help
- **Multiple decorators**: Add examples, commands, colors, and tips
- **Benefits**: Flexible help system, automatic updates with new operations
- **Implementation**: `app/help_decorators.py`

## Error Handling

The application includes comprehensive error handling:

### Custom Exceptions
- **CalculatorError**: Base exception for all calculator errors
- **OperationError**: Errors during mathematical operations
- **ValidationError**: Input validation failures
- **ConfigurationError**: Configuration-related issues

### Error Scenarios Handled
- Division by zero
- Invalid mathematical operations (e.g., even root of negative numbers)
- Invalid input formats
- Configuration validation errors
- File I/O errors
- Missing dependencies (graceful degradation)

## Dependencies

### Required Dependencies
- **python-dotenv**: Environment variable management
- **pandas**: CSV file operations and data management

### Optional Dependencies
- **colorama**: Color-coded terminal output
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting

### Dependency Management
The application gracefully handles missing optional dependencies:
- Core functionality works without pandas (CSV features disabled)
- Help system works without colorama (no colors)
- Configuration works without python-dotenv (uses defaults)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-operation`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Commit your changes (`git commit -m 'Add new operation'`)
7. Push to the branch (`git push origin feature/new-operation`)
8. Create a Pull Request

### Adding New Operations
1. Create a new operation class inheriting from `Operation`
2. Implement required methods: `execute()`, `symbol`, `name`, `description`
3. Register the operation in `OperationFactory._operations`
4. Add tests in `tests/test_operations.py`
5. The help system will automatically include the new operation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Andy Lanchipa

## Acknowledgments

- Design patterns implementation inspired by Gang of Four patterns
- Testing methodology follows Python best practices
- CI/CD pipeline based on GitHub Actions best practices
