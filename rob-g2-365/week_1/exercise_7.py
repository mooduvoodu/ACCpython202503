# Exercise 7: Write an if-elif-else chain that determines the state of water based on a temperature value in the variable 
# temp_c (temperature in Celsius):
#    • If temp_c is below 0, print "Frozen (ice)"
#    • Elif temp_c is above 100, print "Gas (steam)"
#    • Else (otherwise between 0 and 100 inclusive), print "Liquid water"
# Try testing your code with temp_c = -5, temp_c = 25, and temp_c = 105 to see the different outputs.

def water_state(temp_c):
  if temp_c < 0:
    return "Frozen (ice)"
  elif temp_c > 100:
    return "Gas (steam)"
  else:
    return "Liquid water"
  
print("Water state at -5 :", water_state(-5))  
print("Water state at 25 :", water_state(25))  
print("Water state at 105 :", water_state(105))  