# Exercise 12: Given the following code:
# a = [100, 200, [300, 400]]
# b = a            # assignment, no real copy
# c = a.copy()     # shallow copy
#    1. What will happen to a, b, and c if you execute a[0] = 111?
#    2. What will happen to a, b, and c if you execute a[2].append(500)?
# Write your answers explaining the state of a, b, and c after each operation. 
# (This is a thought exercise; you can also write a short script to verify.)

#    1. What will happen to a, b, and c if you execute a[0] = 111?

# a[0] will =111, b[0] = 111, c[0] =200

# 2. What will happen to a, b, and c if you execute a[2].append(500)?

# a and b will have 500 added to it.  c will have a copy of the original a.
