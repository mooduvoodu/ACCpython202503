#Exercise 5: Given the following data, use the in operator to answer the questions:
# allowed_users = ["alice", "bob", "charlie"]
# email = "bob@example.com"
# info = {"email": "bob@example.com", "age": 25, "member": True}
#     1. Check if the string "bob" is in the allowed_users list.
#     2. Check if the substring "@" is in the email string.
#     3. Check if the key "age" is in the info dictionary.
#     4. Check if the value False is in the info dictionary.
# (Print out True or False for each of the above checks.)

allowed_users = ["alice", "bob", "charlie"]
email = "bob@example.com"
info = {"email": "bob@example.com", "age": 25, "member": True}

print("bob in allowed_users: ", "bob" in allowed_users)
print("'@' in email: ", '@' in email)
print("age is a key in info: ", 'age' in info.keys())