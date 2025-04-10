# Exercise 17: Write a snippet of code that asks for two numbers and divides the first by the second. 
# Use try and except to handle two potential errors:
#    1. The user might not enter a number (handle ValueError from int() conversion).
#    2. The user might enter 0 for the second number (handle ZeroDivisionError).
# You can simulate the input by assigning values to variables for this exercise, or use actual input() calls if running interactively.
# (In the answer key, you can just show a simulated test with specific values, to avoid interactive input in this static format.)


while True:
  try:
    value_1_str = input("Value 1? ")
    value_1 = int(value_1_str)
    value_2_str = input("Value 2? ")
    value_2 =  int(value_2_str)
    print("Result = ", value_1 /value_2)
  except ValueError as e:
    print(e)
  except ZeroDivisionError as e:
    print(e)   