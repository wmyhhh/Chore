class Account:
    interest = 0.02
    def __init__(self, name):
        self.account = name
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            return 'you"broke!!'
        self.balance -= amount
        return self.balance

# inheritance
# method for relating two similar classes together
class checkaccount(Account):
    interest = 0.01
    withdraw_fee = 1
    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_fee)

'''
>>> a = Account('frog')
>>> b = checkaccount('snake')
>>> a.deposit(100)
100
>>> b.deposit(100)
100
>>> a.withdraw(100)
0
>>> b.withdraw(99)
0
'''