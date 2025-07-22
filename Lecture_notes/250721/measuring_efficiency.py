def fib(n):
    if n == 0 or n == 1:
        return n 
    else:
        return fib(n - 2) + fib(n - 1)
    
def count(f):
    def counted(n):
        counted.call_amount += 1
        return f(n)
    counted.call_amount = 0
    return counted

'''
>>> fib = count(fib)
>>> fib(40)
102334155
>>> fib(5)
5
>>> fib(10)
55
>>>'''

# memoization
def memo(f):
    cache = {}
    def memorized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memorized


'''
fib (最外层 count)
 └── memo
     └── counted_fib (第一次 count)
         └── original fib
| 赋值语句             | fib 绑定的是                     |
| ------------------- | ---------------------------------- |
| 初始定义             | 原始递归函数                        |
| `fib = count(fib)`  | `count(original_fib)`              |
| `counted_fib = fib` | 保存 `count(original_fib)`          |
| `fib = memo(fib)`   | `memo(count(original_fib))`        |
| `fib = count(fib)`  | `count(memo(count(original_fib)))` |

>>> fib(30)
832040
>>> fib = count(fib)
>>> counted_fib = fib
>>> fib = memo(fib)
>>> fib = count(fib)
>>> fib(30)
832040
>>> fib.call_amount
59
>>> counted_fib.call_amount
31
         '''
