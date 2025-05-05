# Exercise 1:
# amount = 100
#def calc_tax:
    # Amount tax rate
    #rate = 0.1
    #tax = float(amount) * float(rate)
    #print ("Tax: ",tax)
#calc_tax = (amount)

# Excercise 2:
#1.  An integer variable named months with the value 12.
months = 12  #int

#2.	A float variable named temperature with the value 36.6.
temperature = 36.6  #float

#3.	A string variable named message with the value "Hello".
message = "Hello"  #str

#4.	A list variable named colors containing three color names as strings.
colors = ["red", "blue", "green"]  # list of strings

#5.	A dictionary variable named book with keys "title", "author", and "year" representing a book's information.
book = {"title": "The Devil in the White City", "author": "Erik Larson", "year": "2003"}

print(months)
print(temperature)
print(message)
print(colors)
print(book)
# Output: 
# 12, 36.6, Hello, ['red', 'blue', 'green'], {'title': 'The Devil in the White City', 'author': 'Erik Larson', 'year': '2003'}

# Excercise 3:
#   total_cost = valid python name.
#	3d_model = not valid, starts with an interger.
#	playerOne = valid, but better to use snake or pascal case
#	def = not valid, reserved keyword.
#	email_address = valid.
#	first-name = not valid, uses hyphen.
#	PI = valid.

# Excercise 4:
length_str = "15"
width_str = "8.4"
area = float(length_str) * float(width_str)
print("The area of the rectangle is ",area)
# Output: The area of the rectangle is  126.0

# Exercise 5:
allowed_users = ["alice", "bob", "charlie"]
email = "bob@example.com"
info = {"email": "bob@example.com", "age": 25, "member": True}
#1.	Check if the string "bob" is in the allowed_users list.
print("bob" in allowed_users)

#2.	Check if the substring "@" is in the email string.
print('@' in email)

#3.	Check if the key "age" is in the info dictionary.
print("age" in info)

#4.	Check if the value False is in the info dictionary.
print("False" in info)

# Output: True, True, True, False

# Exercise 6
data = [10, 20, 30, 40, 50, 60]
s = "abcdefg"

#1.	Get the first three elements of data using slicing.
print(data[0:3], s[0:3]) # output: [10, 20, 30] abc

#2.	Get the last two elements of data using slicing.
print(data[4:], s[5:]) # output: [50, 60] fg

#3.	Get every other element of data (alternate elements) using slicing.
print(data[::2], s[::2]) # output: [10, 30, 50] aceg

#4.	Get the substring "cde" from the string s using slicing.
print(s[2:5])  # output: cde

#5.	Reverse the string s using slicing.
print(s[::-1])  # output: gfedcba

# Exercise 7
temp_c = 150

if temp_c < 0:
    print("Frozen (ice)")
elif temp_c > 100:
    print("Gas (steam)")
else:
    print("Liquid")

# Output: temp_c = -5, Frozen (ice)
# Output: temp_c = 150, Gas (steam)
# Output: temp_c = 6, Liquid

# Exercise 8
# calculate the sum of all numbers in the list values = [3, 7, 1, 12, 9]. Print the sum after the loop.
values = [3, 7, 1, 12, 9]
total = 0

for n in values:
    total += n

print ("Sum: ", total) #output: 32

# Exercise 9
n = 1
while n <= 5:
    print (n)
    n += 1

# output: 1, 2, 3, 4, 5

# Exercise 10

def square(x: (int,float)) -> (int,float):

    if not isinstance(x, (int,float)):
        print("Error, x must be an interger or float")
        return None
    return x*x

print(square(5))
print(square(2.5))
print(square("5"))

# output: 25, 6.25, Error, x must be an interger or float, None

# Exercise 11
class Book:
    def __init__ (self, title, author):
        self.author = author 
        self.title = title

    def greet(self):
        print(f"My favorite books are {self.title} by {self.author}.")

# Create instances of a book.
b1 = Book ("The Devil in the White City", "Erik Larson")
b2 = Book ("Harry Potter", "J.K. Rowling")

print(b1.title)
print(b2.author)

b1.greet()
b2.greet()

# output: The Devil in the White City
# J.K. Rowling
# My favorite books are The Devil in the White City by Erik Larson.
# My favorite books are Harry Potter by J.K. Rowling.

# Exercise 12

import copy

original = [1, 2, [3, 4]]
assigned = original
shallow_copy = original.copy()
deep_copy = copy.deepcopy(original)

original[2].append(5)

print("Original:", original)
print("Assigned:", assigned)
print("Shallow Copy:", shallow_copy)
print("Deep Copy: ", deep_copy)

# Actual exercise
a = [100, 200, [300, 400]]
b = a
c = a.copy()
d = copy.deepcopy(a)

a[0] = 111
a[2].append(500)

print(a, b, c, d)

# Response: 
# 1.	What will happen to a, b, and c if you execute a[0] = 111? 
#    - a[0] becomes 111 instead of 100
# 2.	What will happen to a, b, and c if you execute a[2].append(500)?
#    - a will become [100, 200, 500, [300, 400]]
# b will be the same as a and c will show original a list and 500.

# Exercise 13
