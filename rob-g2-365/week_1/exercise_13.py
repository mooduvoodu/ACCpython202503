# Exercise 13: Suppose you have a list of integers nums = [5, 8, 12, 15, 7, 1]. 
# Write a line of code using filter and a lambda to create a new list greater_than_10
# that contains only the numbers from nums that are greater than 10. Print the result.
# (Hint: The lambda should return True for numbers that should be kept.)

nums = [5, 8, 12, 15, 7, 1]

greator_than_10 = list(filter(lambda value: value> 10, nums))

print("greator_than_10: ", greator_than_10)