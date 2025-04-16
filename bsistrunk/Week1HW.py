#Exercise 1
# messy code
Amt= 100
DEF calc_tax(amount):
    rate=0.1
    Tax= amount * rate
    print("tax:",Tax)
calc_tax(Amt)


# cleaned code
amount = 100
def calc_tax(amount):
    rate=0.1
    tax = amount * rate
    print("Tax:",tax)
calc_tax(amount)


#Exercise 2
months = 12
temperature = 36.6
message = 'Hello'
colors = ['blue','maroon','white']
book = {"title":"Harry Potter & The Sorcerer's Stone", "author":"J.K. Rowling", "year":"1998"}

print(months)
print(temprerature)
print(message)
print(colors)
print(book)


#Exercise 3
total_cost - Valid
3d_model - Invalid
playerOne - Valid
def - Invalid
email_address - Valid
first-name - Invalid
PI - Valid


#Exercise 4
length_str = "15"
width_str = "8.4"

length = int(length_str)
width = float(width_str)

area = length * width

print("Area:", area)


#Exercise 5
allowed_users = ["alice", "bob", "charlie"]
email = "bob@example.com"
info = {"email": "bob@example.com", "age": 25, "member": True}

#1.	Check if the string "bob" is in the allowed_users list.
print('bob' in allowed_users)
#2.	Check if the substring "@" is in the email string.
print('@' in email)
#3.	Check if the key "age" is in the info dictionary.
print('age' in info)
#4.	Check if the value False is in the info dictionary.
print('False' in info)


#Exercise 6
data = [10, 20, 30, 40, 50, 60]
s = "abcdefg"

#1.	Get the first three elements of data using slicing.
print(data[:3])
#2.	Get the last two elements of data using slicing.
print(data[-2:])
#3.	Get every other element of data (alternate elements) using slicing.
print(data[::2])
#4.	Get the substring "cde" from the string s using slicing.
print(s[2:5])
#5.	Reverse the string s using slicing.
print(s[::-1])


#Exercise 7
temp_c = -5

if temp_c < 0:
    print("Frozen (ice)")
elif temp_c > 100:
    print("Gas(steam)")
else:
    print("Liquid(water)")

temp_c = 25

if temp_c < 0:
    print("Frozen (ice)")
elif temp_c > 100:
    print("Gas(steam)")
else:
    print("Liquid(water)")

temp_c = 105

if temp_c < 0:
    print("Frozen (ice)")
elif temp_c > 100:
    print("Gas(steam)")
else:
    print("Liquid(water)")


#Exercise 8
values = [3, 7, 1, 12, 9]
total = 0
for num in values:
    total += num
print("Sum:", total)


#Exercise 9
counter = 1
while counter <= 5:
    print(counter)
    counter += 1


#Exericse 10
def square(x: (int, float)):
    if not isinstance(x, (int, float)):
        print("Error: x must be a number (int or float)")
        return None
    return x * x

print(square(2.5))


#Exercise 11
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def description(self):
        return f"\"{self.title}\" by {self.author}"
my_book = Book("To Kill a Mockingbird", "Harper Lee")
print(my_book.description())


#Exercise 12
a = [100, 200, [300, 400]]
b = a
c = a.copy()

#1.	What will happen to a, b, and c if you execute a[0] = 111?
    #a = [111, 200, [300, 400]]
#2.	What will happen to a, b, and c if you execute a[2].append(500)?
    #a = [111, 200, [300, 400, 500]]


#Exercise 13
nums = [5, 8, 12, 15, 7, 1]
greater_than_10 = list(filter(lambda n: n > 10, nums))
print(greater_than_10)


#Exercise 14
value = 100

def change_value(value):
    value = 20
    print("Inside function, value =", value)

change_value(value)
print("Outside function, value =", value)