import time
import copy

class Block:

    def __init__(self, transactions, lastHash, forger, blockCount):
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ''
    
    @staticmethod
    def genesis():
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        data = {}
        data['lastHash'] = self.lastHash
        data['forger'] = self.forger
        data['blockCount'] = self.blockCount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        return data
    
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        self.signature = signature
