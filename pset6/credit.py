import math

while True:
    number = int(input("Number: "))
    if str(number).isdigit():
        break
    
sum = 0
temp = number
for i in range(len(str(number)), 0, -2):
    from_last = math.floor(temp%10)
    temp /= 10
    from_sec_to_last = 2 * math.floor(temp % 10)
    temp /= 10
    if from_sec_to_last < 10:
        sum += from_last + from_sec_to_last
    else:
        sum += from_last + 1 + from_sec_to_last % 10

if sum % 10 == 0:
    if len(str(number)) == 15 and (str(number)[0:2] == "34" or str(number)[0:2] == "37"):
        print("AMEX")
    elif len(str(number)) == 16 and str(number)[0:2] in str(list(range(51, 56))):
        print("MASTERCARD")
    elif (len(str(number)) == 13 or len(str(number)) == 16) and str(number)[0:1] == "4":
        print("VISA")
    else:
        print("INVALID")
else: 
    print("INVALID")