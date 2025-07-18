from inheritance import *

class savingaccount(Account):
    deposit_fee = 2
    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_fee)
    
class AsseenOnTVaccount(savingaccount, checkaccount):
    def __init__(self, name):
        self.account = name
        self.balance = 0.8