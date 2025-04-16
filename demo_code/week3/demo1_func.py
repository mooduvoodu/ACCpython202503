# PYTHON FUNCTION AND SCOPE DEMONSTRATION
# --------------------------------------
# This single code file demonstrates various Python concepts about functions,
# scoping rules, variable lifetimes, function arguments, nested functions,
# first-class function objects, closures, decorators, and the use of *args/**kwargs.

# ------------------------------------------------------------------------------
# 1) FUNCTIONS
# ------------------------------------------------------------------------------
# Functions in Python are created with the 'def' keyword and can return values
# with 'return'. Below, we define a simple function and call it.

def foo_basic():
    return 1

print("1) FUNCTIONS")
print(foo_basic())  # Prints: 1
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 2) SCOPE
# ------------------------------------------------------------------------------
# In Python, each function has its own local scope (or namespace). Python looks
# for variable names first in the function's local scope, then searches enclosing
# scopes if not found there.
#
# The globals() function returns a dictionary of all names in the global scope.
# The locals() function returns a dictionary of all names in the local scope.

a_string = "This is a global variable"

def foo_scope():
    # Print local variables in the function
    print("Inside foo_scope, locals():", locals())

print("2) SCOPE")
print("Globals:", list(globals().keys()))  # Printing just the keys for brevity
foo_scope()                                # Prints an empty dict for locals
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 3) VARIABLE RESOLUTION RULES
# ------------------------------------------------------------------------------
# By default, Python will look for a local variable, and if not found, it will
# look for a global. If we access (read) a global variable in a function, it is found;
# however, assigning to a variable in a function by default creates a local variable.

a_string = "This is a global variable"

def foo_resolution():
    # This simply prints the global a_string, since no local variable is defined
    print(a_string)

print("3) VARIABLE RESOLUTION RULES")
foo_resolution()  # Prints: "This is a global variable"

# Now let's see what happens if we try to assign to a_string within a function
a_string = "This is a global variable"

def foo_assignment():
    a_string = "test"  # Shadows the global a_string; creates local variable
    print("Inside foo_assignment, locals():", locals())

foo_assignment()        # Shows a_string is 'test' in the local scope
print("Global a_string is still:", a_string)  # Remains unchanged
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 4) VARIABLE LIFETIME
# ------------------------------------------------------------------------------
# Local variables only exist while the function is executing. After the function
# finishes, its local variables are gone.

def foo_lifetime():
    x = 1
    # When foo_lifetime finishes, x no longer exists

foo_lifetime()
print("4) VARIABLE LIFETIME")
try:
    print(x)  # This will raise a NameError because x is out of scope
except NameError as e:
    print("NameError as expected:", e)
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 5) FUNCTION ARGUMENTS AND PARAMETERS
# ------------------------------------------------------------------------------
# Functions can take positional (mandatory) and named parameters (with default values).

def foo_args(x, y=0):
    return x - y

print("5) FUNCTION ARGUMENTS AND PARAMETERS")
print(foo_args(3, 1))       # Passing both parameters by position => 2
print(foo_args(3))          # y defaults to 0 => 3
try:
    foo_args()              # Missing the mandatory positional argument x
except TypeError as e:
    print("TypeError as expected:", e)

print(foo_args(y=1, x=3))   # Named arguments => 2
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 6) NESTED FUNCTIONS
# ------------------------------------------------------------------------------
# Python allows functions to be declared inside other functions. The inner function
# has access to the enclosing scope (read and modify if mutable).

def outer_function():
    x = 1
    def inner_function():
        # Looks for x in inner_function's locals, doesn't find it,
        # then finds it in outer_function's scope
        print(x)
    # We call the inner function within outer_function
    inner_function()

print("6) NESTED FUNCTIONS")
outer_function()  # Prints: 1
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 7) FUNCTIONS ARE FIRST-CLASS OBJECTS
# ------------------------------------------------------------------------------
# In Python, everything is an object, including functions. This means we can
# assign functions to variables, pass them as arguments to other functions,
# and return them from functions.

def foo_object():
    pass

print("7) FUNCTIONS ARE FIRST-CLASS OBJECTS")
print("Type of foo_object is:", type(foo_object))



# Demonstration: we can pass functions as arguments to another function
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def apply(func, x, y):
    return func(x, y)

print(apply(add, 2, 1))  # 3
print(apply(sub, 2, 1))  # 1
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 8) CLOSURES
# ------------------------------------------------------------------------------
# A closure is created when an inner function remembers the state of its enclosing
# scope even after the outer function has finished execution.

def outer_closure():
    x = 1
    def inner():
        print(x)
    return inner

print("8) CLOSURES")
foo_closure = outer_closure()
foo_closure() # Prints 1, even though outer_closure has finished

# Multiple versions of an inner function can each "remember" their own values:
def outer_closure_param(x):
    def inner():
        print(x)
    return inner

print1 = outer_closure_param(1)
print2 =  outer_closure_param(2)
print1()  # 1
print2()  # 2
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 9) DECORATORS
# ------------------------------------------------------------------------------
# A decorator is a callable that takes a function as an argument and returns a
# replacement (wrapped) function. It's a way to modify or enhance the behavior
# of functions without changing their code.

def outer_decorator(some_func):
    def inner():
        print("before some_func")
        ret = some_func()  # Call the original function
        return ret + 1      # Modify the return value
    return inner

def foo_decor():
    return 1

decorated = outer_decorator(foo_decor)
print("9) DECORATORS")
print(decorated())  # Prints the message and returns 2

# We can also reassign foo_decor to its decorated version:
foo_decor = outer_decorator(foo_decor)
print(foo_decor())  # This now has the decorated behavior
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 10) USING THE @ SYMBOL TO APPLY A DECORATOR
# ------------------------------------------------------------------------------
# Python allows syntactic sugar for decorators using the @ symbol. This is exactly
# equivalent to reassigning the function name to the result of the decorator call.

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "Coord: " + str(self.__dict__)

def add_coord(a, b):
    return Coordinate(a.x + b.x, a.y + b.y)

def sub_coord(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)

one = Coordinate(100, 200)
two = Coordinate(300, 200)
three = Coordinate(-100, -100)

# Let's write a decorator to ensure no negative coordinates
def wrapper_bounds(func):
    def checker(a, b):
        # Adjust inputs if negative
        if a.x < 0 or a.y < 0:
            a = Coordinate(max(a.x, 0), max(a.y, 0))
        if b.x < 0 or b.y < 0:
            b = Coordinate(max(b.x, 0), max(b.y, 0))

        ret = func(a, b)

        # Adjust output if negative
        if ret.x < 0 or ret.y < 0:
            ret = Coordinate(max(ret.x, 0), max(ret.y, 0))

        return ret
    return checker

# Using the @ syntax to apply the decorator:
@wrapper_bounds
def add_checked(a, b):
    return Coordinate(a.x + b.x, a.y + b.y)

@wrapper_bounds
def sub_checked(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)

print("10) THE @ SYMBOL APPLIES A DECORATOR TO A FUNCTION")
print(sub_checked(one, two))   # Should clamp negatives to 0
print(add_checked(one, three)) # Also clamps negatives to 0
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 11) *args AND **kwargs
# ------------------------------------------------------------------------------
# *args captures additional positional arguments. **kwargs captures additional
# keyword arguments. They can be used both in function definitions and calls,
# enabling flexible argument passing.

def example_args(*args):
    print("Positional args are:", args)

def example_kwargs(**kwargs):
    print("Keyword args are:", kwargs)

print("11) *args AND **kwargs")
example_args()
example_args(1, 2, 3)

example_kwargs()
example_kwargs(x=1, y=2)

# Using * in a function call to expand a list into positional args:
def add_xy(x, y):
    return x + y

lst = [1, 2]
print("add_xy(*lst):", add_xy(*lst))  # 3

# Using ** in a call to expand a dict into keyword arguments:
dct = {'x': 1, 'y': 2}
print("add_xy(**dct):", add_xy(**dct))  # 3
print("--------------------------------------------------\n")


# ------------------------------------------------------------------------------
# 12) MORE GENERIC DECORATORS WITH *args AND **kwargs
# ------------------------------------------------------------------------------
# A decorator that logs arguments can wrap any function regardless of signature
# by capturing all positional and keyword arguments.

def logger(func):
    def inner(*args, **kwargs):
        print(f"Arguments were: {args}, {kwargs}")
        return func(*args, **kwargs)
    return inner

@logger
def foo1(x, y=1):
    return x * y

@logger
def foo2():
    return 2

print("12) MORE GENERIC DECORATORS")
print(foo1(5, 4))  # Logs arguments and returns 20
print(foo1(1))     # Logs arguments and returns 1
print(foo2())      # Logs arguments and returns 2
print("--------------------------------------------------\n")


# PYTHON DOES NOT FORCE DATA TYPES BY DEFAULT
# -----------------------------------------------------------
# Python is a dynamically typed language, meaning it does not
# enforce types at compile time. You can pass any object to a
# function, and only operations that are invalid for that type
# will fail at runtime.

def add_numbers(a, b):
    """
    Demonstrates Python's dynamic typing:
    - Can add integers, concatenate strings, etc.
    - Will raise a TypeError only if the operation is invalid.
    """
    return a + b

print("=== Dynamic Typing Demo ===")
print("add_numbers(1, 2) =>", add_numbers(1, 2))           # 3
print("add_numbers('Hello', ' World') =>", add_numbers("Hello", " World"))  # "Hello World"
try:
    print("add_numbers('Hello', 2) =>", add_numbers("Hello", 2))  # TypeError
except TypeError as e:
    print("TypeError as expected:", e)
print()


# TYPE HINTS (OPTIONAL STATIC ANALYSIS)
# -----------------------------------------------------------
# Python 3.5+ allows type hints (annotations). These hints are
# NOT enforced at runtime by default. Instead, they're useful
# for IDEs, linters, or external tools (e.g., mypy) to provide
# static type checking.

def add_numbers_typed(a: int, b: int) -> int:
    """
    Function using type hints:
    - Intended for (a, b) as ints, returning int.
    - Python will still let you pass any type at runtime, unless
      you use an additional checking library or tool.
    """
    return a + b

print("=== Type Hints Demo ===")
print("add_numbers_typed(3, 4) =>", add_numbers_typed(3, 4))  # 7
print("No error if we pass strings here at runtime, but a static checker would warn.")
print()


# RUNTIME ENFORCEMENT (THIRD-PARTY EXAMPLES)
# -----------------------------------------------------------
# Example 1: typeguard
#   pip install typeguard
#
# from typeguard import typechecked
#
# @typechecked
# def add_numbers_typeguard(a: int, b: int) -> int:
#     return a + b
#
# print("=== typeguard Demo ===")
# print(add_numbers_typeguard(5, 6))      # 11
# print(add_numbers_typeguard("Hello", 2))  # Raises TypeCheckError at runtime
#
# Example 2: enforce
#   pip install enforce
#
# from enforce_typing import enforce_types
#
# @enforce_types
# def add_numbers_enforced(a: int, b: int) -> int:
#     return a + b
#
# print("=== enforce Demo ===")
# print(add_numbers_enforced(5, 6))        # 11
# print(add_numbers_enforced("Hello", 2))  # Raises a TypeError at runtime
#
# Uncomment the lines above after installing the respective library
# to see runtime-enforced type checks in action.


# MANUAL TYPE ENFORCEMENT
# -----------------------------------------------------------
# You can also manually enforce types within the function body.
# This is the most explicit way, though it's more verbose and not
# typically used unless truly needed.

def add_numbers_strict(a, b):
    """
    Manually checks the types of a and b before proceeding.
    If they are not integers, raises TypeError.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both a and b must be int.")
    return a + b

print("=== Manual Type Check Demo ===")
print("add_numbers_strict(5, 6) =>", add_numbers_strict(5, 6))  # 11
try:
    print(add_numbers_strict("Hello", 2))
except TypeError as e:
    print("TypeError as expected:", e)

# SUMMARY
# -----------------------------------------------------------
# 1. By default, Python is dynamically typed: no compile-time type checks.
# 2. You can add type hints for clarity and optional static analysis.
# 3. For runtime enforcement, either:
#    - Use a third-party tool like 'typeguard' or 'enforce'.
#    - Manually validate types inside your function.



"""
DEMO: Object-Oriented vs. Functional-Style Solutions in Python

We'll solve the same simple problem—calculating the total area of
a list of shapes—in two ways:

1) Object-Oriented (OOP) Approach
2) Functional Approach
"""

# --------------------------------------------------------
# 1) OBJECT-ORIENTED APPROACH
# --------------------------------------------------------
# In the OOP style, each shape is represented as a class with
# an area() method. We create instances of these classes and
# then aggregate their areas.

import math

class Shape:
    """Base class for shapes."""
    def area(self):
        raise NotImplementedError("Subclasses should implement this.")

class Circle(Shape):
    """Circle with a given radius."""
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

class Rectangle(Shape):
    """Rectangle with a given width and height."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

# Create instances of shapes
shapes_oop = [
    Circle(2),
    Circle(3),
    Rectangle(4, 5),
    Rectangle(2, 6)
]

# Calculate total area by calling the area() method on each shape
total_area_oop = sum(shape.area() for shape in shapes_oop)

print("=== OOP APPROACH ===")
for s in shapes_oop:
    print(f"{s.__class__.__name__} area: {s.area():.2f}")
print(f"Total OOP area: {total_area_oop:.2f}")
print()


# --------------------------------------------------------
# 2) FUNCTIONAL APPROACH
# --------------------------------------------------------
# In the functional style, we represent shapes with basic data
# structures (e.g., dictionaries). We then define separate
# functions that operate on those structures. No classes or
# methods—just data plus functions.

# We'll encode a shape as a dict with a 'type' key and any
# necessary parameters (e.g., 'radius', 'width', 'height').

def area_functional(shape):
    """
    Compute the area of a shape dict.
    shape['type'] can be 'circle' or 'rectangle'.
    """
    if shape["type"] == "circle":
        # shape expects 'radius'
        return math.pi * (shape["radius"] ** 2)
    elif shape["type"] == "rectangle":
        # shape expects 'width' and 'height'
        return shape["width"] * shape["height"]
    else:
        raise ValueError(f"Unknown shape type: {shape['type']}")

shapes_functional = [
    {"type": "circle",    "radius": 2},
    {"type": "circle",    "radius": 3},
    {"type": "rectangle", "width": 4, "height": 5},
    {"type": "rectangle", "width": 2, "height": 6},
]

# Compute total area by applying the area_functional to each shape
total_area_functional = sum(area_functional(s) for s in shapes_functional)

print("=== FUNCTIONAL APPROACH ===")
for s in shapes_functional:
    print(f"{s['type'].capitalize()} area: {area_functional(s):.2f}")
print(f"Total Functional area: {total_area_functional:.2f}")
