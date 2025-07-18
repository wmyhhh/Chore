from inheritance import *
class Bank:
    '''
    >>> bank = Bank()
    >>> a = bank.open_account('juliet', 10)
    >>> b = bank.open_account('romeo', 15, checkaccount)
    >>> a.interest
    0.02
    >>> b.interest
    0.01
    >>> bank.pay_interest()
    >>> a.balance
    10.2
    >>> b.balance
    15.15
    '''
    def __init__(self):
        self.accounts = []

    def open_account(self, name, amount, kind = Account):
        account = kind(name)
        account.deposit(amount)
        self.accounts.append(account)
        return account
    
    def pay_interest(self):
        for i in self.accounts:
            i.deposit(i.balance * i.interest)

    