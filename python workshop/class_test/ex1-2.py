side1 = int(input())
side2 = int(input())
side3 = int(input())

# 判断是否构成三角形
if side1 + side2 > side3 and side1 + side3 > side2 and side2 + side3 > side1:
    # 判断三角形类型
    if side1 == side2 == side3:
        print("E")
    elif side1 == side2 or side1 == side3 or side2 == side3:
        print("I")
    elif side1**2 + side2**2 == side3**2 or side1**2 + side3**2 == side2**2 or side2**2 + side3**2 == side1**2:
        print("R")
    else:
        print("S")
else:
    print("N")