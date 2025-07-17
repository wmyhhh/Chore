# methods are invoked by dot notation: <expression>.<name>
# then call the method on ...： <expression>.<name>(10)

class Account:
    def __init__(self, name):
        self.account = name
        self.balance = 0
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    def withdraw(self, amount):
        if amount > self.balance:
            return 'you"are broke!!!'
        self.balance -= amount
        return self.balance
    

'''
>>> a = Account('alpha')
>>> a
<__main__.Account object at 0x000001E9F9B2CA90>
>>> f = a.deposit
>>> f
<bound method Account.deposit of <__main__.Account object at 0x000001E9F9B2CA90>>
>>> k = map(f,range(1,10))
>>> next(k)
1
>>> list(k)
[3, 6, 10, 15, 21, 28, 36, 45]
>>>
'''

# attribute lookup
'''
>>> getattr(a, 'balance')
45
>>> hasattr(a, 'balance')
True
>>> getattr(a, 'withdraw')
<bound method Account.withdraw of <__main__.Account object at 0x000001E9F9B2CA90>>
>>> getattr(a, 'withdraw')(10)
35
>>>
'''

# class attribute
class account:
    interest = 0.02   # class attribute shared by every object of this class
    def __init__(self):
        pass

# bound method: class attribute & function
# object + function = bound method
'''
>>> type(Account.deposit)
<class 'function'>
>>> type(a.deposit)
<class 'method'>

>>> Account.deposit(a,100)
135
>>> a.deposit(100)
235
'''

# class attribute vs instance attribute
'''
>>> a = Account('Alcaraz')
>>> b = Account('Sinner')
>>> Account.interest = 0.5
>>> a.interest
0.5
>>> b.interest
0.5
>>> a.interest = 0.8
>>> Account.interest = 0.3
>>> a.interest
0.8
>>> b.interest
0.3
>>>
'''