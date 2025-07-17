# object oriented programming
# object is an instance of a class, the class is its type
# class defines how obects of a particular type behave
# method is a function called on an object using an dot expression  e.g. s.append(5)

'''
>>> list
<class 'list'>
>>> l = list(range(3))
>>> l
[0, 1, 2]
>>> type(l)
<class 'list'>
'''
# creating class
class Account:
    def __init__(self, holder):
        self.account = holder
        self.balance = 0
    def deposit(self, amount):
        self.balance += amount
        return 
    def withdraw(self, amount):
        if amount > self.balance:
            return "you're broke"
        self.balance -= amount
        return self.balance
    
# creating instance
'''
>>> b = Account('adam')
>>> a.backup = b
>>> b.deposit(100)
>>> b.balance
100
>>> a.backup.balance
100
'''
s = [6, 7, 8]
print(s.append(6))