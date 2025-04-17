# Exercise 1:
amount = 100
def_calc_tax:
    # Amount tax rate
    rate = 0.1
    tax = float(amount) * float(rate)
    print ("Tax: ",tax)
def_calc_tax = (amount)

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
