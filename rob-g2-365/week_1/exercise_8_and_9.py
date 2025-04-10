#Exercises 8 and 9: Practice with loops:
#    • Exercise 8: Using a for loop, calculate the sum of all numbers in the list values = [3, 7, 1, 12, 9]. 
#      Print the sum after the loop.

values = [3, 7, 1, 12, 9]
sum = 0
for value in values:
    sum += value

print("sum: ", sum)    


#  • Exercise 9: Using a while loop, print the numbers 1 through 5 (inclusive). 
# (Hint: Initialize a counter variable to 1, and loop while it’s <= 5, printing the counter and incrementing it by 1 each iteration.)

index = 0
while(index<len(values)):
    print("value: ", values[index])
    index+=1

    