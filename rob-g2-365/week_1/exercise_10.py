# Exercise 10: Write a function called square() that takes one parameter (a number) 
# and returns the square of that number. Include a type hint indicating the parameter should be a number 
# (int or float) and the return type is a number. Then, call your function with a couple of examples 
# (e.g., square(5), square(2.5)) and print the results.
# Bonus: Inside the function, add a check to ensure the argument is an int or float, and print a friendly error message if not.

def square(number: float | int) ->  float | int:
  return number * number

print("square(5) :", square(5))
print("square(2.5) :", square(2.5))
print("square('hello') :", square('hello'))
