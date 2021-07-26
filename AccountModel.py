from Crypto import PublicKey


class AccountModel:
    
    def __init__(self):
        self.accounts = []
        self.balances = {}

    def addAccount(self, publicKeyString):
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0
        
    def getBalance(self, publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]
    
    def updateBalance(self, publicKeyString, amount):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount
