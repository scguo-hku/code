import math

# Initialize variables
sum_of_numbers = 0
count = 0

while True:
    number = int(input())
    if number == 0:
        break
    sum_of_numbers += number
    count += 1


average = sum_of_numbers / count
floored_average = math.floor(average)
print(floored_average)
