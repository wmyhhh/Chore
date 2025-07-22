# exponentiel -> O(x ** n)  e.g. fib(n)
# a * (x ** (n + 1)) = a * (x ** n) * x
def fib(n):
    if n == 1 or n == 0:
        return n
    else:
        return fib(n - 2) + fib(n - 1)

# quadratic  -> O(n ** 2)
# a * (x + 1) ** 2 = a * x ** 2 + 2 * a * x + a
def pair(l, k):
    cnt = 0
    for i in l:
        for j in k:
            if i == j:
                cnt += 1
    return cnt

# linear  -> O(n)  e.g. slow_exp
# a * (x + 1) = a * x + a

# logrithmic  -> O(log n)  e.g. fast_exp
# a * ln(2 * x) = a * ln(x) + a * ln2

# constant  -> O(1)  e.g. dict


# with the help of GPT
import time
import matplotlib.pyplot as plt
import math

# --- 复杂度函数定义 ---

# 指数复杂度
def fib(n):
    if n == 0 or n == 1:
        return n
    return fib(n - 1) + fib(n - 2)

# 二次复杂度
def pair(l1, l2):
    cnt = 0
    for i in l1:
        for j in l2:
            if i == j:
                cnt += 1
    return cnt

# 线性复杂度
def linear(n):
    total = 0
    for i in range(n):
        total += i
    return total

# 对数复杂度
def logarithmic(n):
    cnt = 0
    while n > 1:
        n = n // 2
        cnt += 1
    return cnt

# 常数复杂度
def constant(n):
    return n ** 2 + 1

# --- 测试函数运行时间 ---
def time_func(f, *args):
    start = time.time()
    f(*args)
    return (time.time() - start) * 1000  # 毫秒

# --- 输入规模设置 ---
sizes_fib = list(range(10, 36, 2))  # fib 不能太大
sizes_other = list(range(100, 5100, 500))  # 适用于其他算法

# --- 数据记录 ---
fib_times = [time_func(fib, n) for n in sizes_fib]
pair_times = [time_func(pair, list(range(n)), list(range(n))) for n in sizes_other]
linear_times = [time_func(linear, n) for n in sizes_other]
log_times = [time_func(logarithmic, n) for n in sizes_other]
const_times = [time_func(constant, n) for n in sizes_other]

# --- 绘图 ---
plt.figure(figsize=(12, 6))

# fib
plt.plot(sizes_fib, fib_times, label="Exponential O(2^n)", color='red', marker='o')

# 其他函数
plt.plot(sizes_other, pair_times, label="Quadratic O(n^2)", color='orange', marker='x')
plt.plot(sizes_other, linear_times, label="Linear O(n)", color='green', marker='s')
plt.plot(sizes_other, log_times, label="Logarithmic O(log n)", color='blue', marker='^')
plt.plot(sizes_other, const_times, label="Constant O(1)", color='purple', linestyle='--')

plt.title("Runtime Growth of Different Complexity Functions")
plt.xlabel("Input Size")
plt.ylabel("Execution Time (ms)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
