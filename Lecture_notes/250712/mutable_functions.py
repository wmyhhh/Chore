# fonction that varies everytime it takes in the same amount
def make_withdraw(balance):
    b = [balance]
    def withdraw(amount):
        if b[0] - amount < 0:
            return "you're broke hahaha"
        b[0] = b[0] - amount
        return b[0]
    return withdraw
'''
>>> withdraw = make_withdraw(100)
>>> withdraw(10)
90
>>> withdraw(10)
80
'''
