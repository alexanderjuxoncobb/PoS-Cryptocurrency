from ProofOfStake import ProofOfStake
from Transaction import Transaction
from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


class Blockchain:

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()
        self.total_remaining = 100000000  # NEW

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def listOfBlocks(self):
        return self.blocks

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block):
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False

    def lastBlockHashValid(self, block):
        latestBlockchainBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        if latestBlockchainBlockHash == block.lastHash:
            return True
        else:
            return False
    
    def getCoveredTransactionSet(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)

            else:
                print('Transaction is not covered by sender.')
        return coveredTransactions

    def transactionCovered(self, transaction):
        if transaction.type == 'EXCHANGE':
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)



# THIS IS WERE YOU MINUS IT FROM THE 10000000.

    def executeTransaction(self, transaction):  # so you need to automate this shit... so it's not 'if it is stake'
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount)
        else:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)
            self.accountModel.updateBalance(receiver, amount)

# need to find a way for the total amount to go down by stake amount each time.

    def listOfForgersPublicKeys(self): # used to be nextForger
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        # possibleForgers = self.pos.validatorLots(lastBlockHash)
        listOfForgersPublicKeys = self.pos.forgers(lastBlockHash)
        # self.possibleForgers = self.pos.validators()
        return listOfForgersPublicKeys
        # return possibleForgers
        # need to make sure the 100 are hosen from next yeah?????
        # NB validators must be called AFTER you have called the next forger, otherwise it doesnt exist.

    #def possibleForgers(self):
        #return self.pos.validators()
            # return self.pos.validators()
        ##return self.possibleForgers

    def createBlock(self, transactionFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(newBlock)
        return newBlock
    
    def transactionExists(self, transaction):
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block):
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        return False

    def transactionValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
