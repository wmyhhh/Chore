def swipe(n):
    """Print the digits of n, one per line, first backward then forward.

    >>> swipe(2837)
    7
    3
    8
    2
    8
    3
    7
    """
    if n < 10:
        print(n)
    else:
        "*** YOUR CODE HERE ***"
        print(n % 10)
        swipe(n // 10)
        print(n % 10)
'''
GPT explains

举例执行流程：swipe(2837)
我们跟踪整个调用：

第一次调用：swipe(2837)
打印 7（2837 % 10）

进入 swipe(283)...

第二次调用：swipe(283)
打印 3（283 % 10）

进入 swipe(28)...

第三次调用：swipe(28)
打印 8

进入 swipe(2)...

第四次调用：swipe(2)（n < 10）
打印 2

返回到上一层...

现在回溯开始了：

回到 swipe(28)：再次打印 8

回到 swipe(283)：再次打印 3

回到 swipe(2837)：再次打印 7

'''
    
def skip_factorial(n):
    """Return the product of positive integers n * (n - 2) * (n - 4) * ...

    >>> skip_factorial(5) # 5 * 3 * 1
    15
    >>> skip_factorial(8) # 8 * 6 * 4 * 2
    384
    """
    if n == 1 or n == 2:
        return n
    else:
        return n * skip_factorial(n - 2)
    
def is_prime(n):
    """Returns True if n is a prime number and False otherwise.
    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 2:
        return False
    def f(i):
        if i * i > n:
            return True
        elif n % i == 0:
            return False    
        return f(i + 1)
    return f(2)

