# Exercise 11: Define a class Book with two attributes: title and author (set these in the __init__ method). 
# Add a method description that prints or returns a string like "<title>" by <author>. 
# Create an instance of Book for your favorite book, and call the description method.
# (No need to implement complex logic — just practice creating a class, attributes, and a method.)

class Book:
  def __init__(self, title, author):
    self.title = title
    self.author = author

  def description(self):
    return f"{self.title} by {self.author}"
  

b = Book('Pandas for Everyone', 'Daniel Y. Chen')
print("Description: ", b.description())
