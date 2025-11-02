"""Test cases for operation classes."""

import pytest
import math
from app.operations import (
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation,
    PowerOperation, RootOperation, ModulusOperation, IntegerDivideOperation,
    PercentageOperation, AbsoluteDifferenceOperation, OperationFactory
)
from app.exceptions import OperationError


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    def test_add_operation(self):
        """Test addition operation."""
        add_op = AddOperation()
        assert add_op.execute(5, 3) == 8
        assert add_op.execute(-2, 7) == 5
        assert add_op.execute(0, 0) == 0
        assert add_op.execute(2.5, 1.5) == 4.0
        assert add_op.symbol == "+"
        assert add_op.name == "add"
    
    def test_subtract_operation(self):
        """Test subtraction operation."""
        sub_op = SubtractOperation()
        assert sub_op.execute(10, 3) == 7
        assert sub_op.execute(5, 8) == -3
        assert sub_op.execute(0, 5) == -5
        assert sub_op.execute(7.5, 2.5) == 5.0
        assert sub_op.symbol == "-"
        assert sub_op.name == "subtract"
    
    def test_multiply_operation(self):
        """Test multiplication operation."""
        mul_op = MultiplyOperation()
        assert mul_op.execute(4, 5) == 20
        assert mul_op.execute(-3, 7) == -21
        assert mul_op.execute(0, 100) == 0
        assert mul_op.execute(2.5, 4) == 10.0
        assert mul_op.symbol == "*"
        assert mul_op.name == "multiply"
    
    def test_divide_operation(self):
        """Test division operation."""
        div_op = DivideOperation()
        assert div_op.execute(10, 2) == 5
        assert div_op.execute(15, 3) == 5
        assert div_op.execute(7, 2) == 3.5
        assert div_op.symbol == "/"
        assert div_op.name == "divide"
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        div_op = DivideOperation()
        with pytest.raises(OperationError):
            div_op.execute(10, 0)


class TestAdvancedOperations:
    """Test advanced mathematical operations."""
    
    def test_power_operation(self):
        """Test power operation."""
        pow_op = PowerOperation()
        assert pow_op.execute(2, 3) == 8
        assert pow_op.execute(5, 2) == 25
        assert pow_op.execute(10, 0) == 1
        assert pow_op.execute(4, 0.5) == 2
        assert pow_op.symbol == "^"
        assert pow_op.name == "power"
    
    def test_power_edge_cases(self):
        """Test power operation edge cases."""
        pow_op = PowerOperation()
        with pytest.raises(OperationError):
            pow_op.execute(0, -1)  # Zero to negative power
    
    def test_root_operation(self):
        """Test root operation."""
        root_op = RootOperation()
        assert abs(root_op.execute(8, 3) - 2) < 0.0001  # Cube root of 8
        assert abs(root_op.execute(16, 4) - 2) < 0.0001  # 4th root of 16
        assert root_op.execute(1, 5) == 1  # Any root of 1
        assert root_op.symbol == "√"
        assert root_op.name == "root"
    
    def test_root_edge_cases(self):
        """Test root operation edge cases."""
        root_op = RootOperation()
        with pytest.raises(OperationError):
            root_op.execute(5, 0)  # Zero root
        with pytest.raises(OperationError):
            root_op.execute(-4, 2)  # Even root of negative
    
    def test_modulus_operation(self):
        """Test modulus operation."""
        mod_op = ModulusOperation()
        assert mod_op.execute(10, 3) == 1
        assert mod_op.execute(15, 4) == 3
        assert mod_op.execute(8, 2) == 0
        assert mod_op.symbol == "%"
        assert mod_op.name == "modulus"
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        mod_op = ModulusOperation()
        with pytest.raises(OperationError):
            mod_op.execute(10, 0)
    
    def test_integer_divide_operation(self):
        """Test integer division operation."""
        int_div_op = IntegerDivideOperation()
        assert int_div_op.execute(10, 3) == 3
        assert int_div_op.execute(15, 4) == 3
        assert int_div_op.execute(8, 2) == 4
        assert int_div_op.symbol == "//"
        assert int_div_op.name == "int_divide"
    
    def test_integer_divide_by_zero(self):
        """Test integer division by zero raises error."""
        int_div_op = IntegerDivideOperation()
        with pytest.raises(OperationError):
            int_div_op.execute(10, 0)
    
    def test_percentage_operation(self):
        """Test percentage operation."""
        pct_op = PercentageOperation()
        assert pct_op.execute(25, 100) == 25.0
        assert pct_op.execute(50, 200) == 25.0
        assert pct_op.execute(3, 12) == 25.0
        assert pct_op.symbol == "%of"
        assert pct_op.name == "percent"
    
    def test_percentage_with_zero_base(self):
        """Test percentage with zero base raises error."""
        pct_op = PercentageOperation()
        with pytest.raises(OperationError):
            pct_op.execute(10, 0)
    
    def test_absolute_difference_operation(self):
        """Test absolute difference operation."""
        abs_diff_op = AbsoluteDifferenceOperation()
        assert abs_diff_op.execute(10, 3) == 7
        assert abs_diff_op.execute(3, 10) == 7
        assert abs_diff_op.execute(-5, 2) == 7
        assert abs_diff_op.execute(5, 5) == 0
        assert abs_diff_op.symbol == "abs_diff"
        assert abs_diff_op.name == "abs_diff"


class TestOperationFactory:
    """Test operation factory pattern."""
    
    def test_create_valid_operations(self):
        """Test creating valid operations."""
        operations = [
            "add", "subtract", "multiply", "divide", "power",
            "root", "modulus", "int_divide", "percent", "abs_diff"
        ]
        
        for op_name in operations:
            op = OperationFactory.create_operation(op_name)
            assert op.name == op_name
    
    def test_create_invalid_operation(self):
        """Test creating invalid operation raises error."""
        with pytest.raises(OperationError):
            OperationFactory.create_operation("invalid_op")
    
    def test_get_available_operations(self):
        """Test getting available operations."""
        operations = OperationFactory.get_available_operations()
        assert len(operations) == 10
        assert "add" in operations
        assert "divide" in operations
        assert "power" in operations
    
    def test_case_insensitive_operation_creation(self):
        """Test operation creation is case insensitive."""
        add_op1 = OperationFactory.create_operation("ADD")
        add_op2 = OperationFactory.create_operation("add")
        add_op3 = OperationFactory.create_operation("Add")
        
        assert type(add_op1) == type(add_op2) == type(add_op3)
    
    def test_register_new_operation(self):
        """Test registering a new operation."""
        class TestOperation:
            def execute(self, a, b):
                return a + b
            
            @property
            def name(self):
                return "test"
            
            @property
            def symbol(self):
                return "T"
            
            @property
            def description(self):
                return "Test operation"
        
        # Note: This would normally inherit from Operation, 
        # but we're testing the validation
        with pytest.raises(OperationError):
            OperationFactory.register_operation("test", TestOperation)
