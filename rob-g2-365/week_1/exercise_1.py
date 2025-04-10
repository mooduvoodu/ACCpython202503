# Exercise 1: The following code has poor style and naming.
# Rewrite it using proper Python style and naming conventions:

# messy code
# Amt= 100
# DEF calc_tax(amount):
#    rate=0.1
#    Tax= amount*rate
#    print("tax:",Tax)
# calc_tax(Amt)

amt = 100
def calc_tax(amount):
    rate = 0.1
    tax = amount*rate
    print("tax:", tax)
calc_tax(amt)
