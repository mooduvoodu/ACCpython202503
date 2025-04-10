#Exercise 14: What will the following code print, and why?
value = 100

def change_value(value):
    value = 20
    print("Inside function, value =", value)

change_value(value)
print("Outside function, value =", value)

# Inside function, value =20
# Outside function, value 100

# After understanding the output, how would you modify change_value to actually change the global value? (Answer in words or code.)

# Could just rename the parameter to something other then value.  Could have the function return value and the caller set it to value.


