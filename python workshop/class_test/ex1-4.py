# 输入一个整数 n
n = int(input())

# 初始化前两个斐波那契数
fib_sequence = [0, 1]

# 生成斐波那契数列
for i in range(2, n):
    next_fib = fib_sequence[-1] + fib_sequence[-2]
    fib_sequence.append(next_fib)

# 打印前 n 个斐波那契数
for num in fib_sequence[:n]:
    print(num)