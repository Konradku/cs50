while True:
    height = int(input("Height: "))
    if height > 0 and height < 9:
        break
    
for i in range(1, height+1):
    print((height-i) * " " + i * "#" + 2 * " " + i * "#")