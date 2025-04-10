#Exercise 6: Consider the list data = [10, 20, 30, 40, 50, 60] and the 
# string s = "abcdefg". Write expressions or lines of code to achieve the following:
#     1. Get the first three elements of data using slicing.
#     2. Get the last two elements of data using slicing.
#     3. Get every other element of data (alternate elements) using slicing.
#     4. Get the substring "cde" from the string s using slicing.
#     5. Reverse the string s using slicing.
# (Print the results of each to verify your answers.)

data = [10, 20, 30, 40, 50, 60]

#     1. Get the first three elements of data using slicing.
print("Get the first three elements of data using slicing.", data[:3])

# 2. Get the last two elements of data using slicing.
print("Get the last two elements of data using slicing.", data[-2:])

# Get every other element of data (alternate elements) using slicing.
print("Get every other element of data (alternate elements) using slicing.", data[::2])

s = "abcdefg"

#     4. Get the substring "cde" from the string s using slicing.
print("Get the substring \"cde\" from the string s using slicing. ", s[2:5])

# 5. Reverse the string s using slicing
print("Reverse the string s using slicing. ", s[::-1])