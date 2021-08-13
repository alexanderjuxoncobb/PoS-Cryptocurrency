from BlockchainUtils import BlockchainUtils
from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
import copy
import pprint


class Node:

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.fromKey(key)   # Says that self.keyPair = key.

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature
   
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionValid(block.transactions)
        if not blockCountValid:
            self.requestChain()
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def requestChain(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.broadcast(encodedMessage)
    
    def handleBlockchainRequest(self, requestingNode):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)

    def handleBlockchain(self, blockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)
        if localBlockCount < receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy



    # CURRENT ISSUE: ALL WORKING FINE, HOWEVER NOT MINING BLOCKS AFTER FORST 1


    def thisBlockValid(self, listOfForgersPublicKeys):
        listOfBlocks = []
        transactionFromPool = self.transactionPool.transactions
        coveredTransactions = self.blockchain.getCoveredTransactionSet(transactionFromPool)
        self.blockchain.executeTransactions(coveredTransactions)
        for forger in listOfForgersPublicKeys:
            forgerWallet = Wallet(forger)
            # newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(self.blockchain.blocks[-1].payload()).hexdigest(), len(self.blockchain.blocks))
            newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(self.blockchain.blocks[-1].payload()).hexdigest(), len(self.blockchain.listOfBlocks()))
            # listOfBlocks.append(blockchain.createBlock(coveredTransactions, BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest(), len(self.blocks)))
            listOfBlocks.append(self.blockchain.createBlock(self.transactionPool.transactions, forgerWallet))
        # this doesnt really do anything i dont think. unless i change it to forger as i have done.
        if (listOfBlocks[0] == listOfBlocks[i] for i in range(len(listOfBlocks) - 1)):
            return True
        else:
            return False

            # issue in here basically saying: str object has on attribute createBlock. I.e. self.blockchain is


    def forge(self):  # so this is running on every node remember.
        listOfForgersPublicKeys = self.blockchain.listOfForgersPublicKeys()  # remember this is more than one of them. NB this is a publicKey
        forgerPublicKey = listOfForgersPublicKeys[0]

        #possibleForgers = self.blockchain.possibleForgers  # need to maybe say that if it is all the same, we should return True + the shit below???????
        
        # pprint.pprint(possibleForgers)
        # print(self.possibleForgers)
        
        if forgerPublicKey == self.wallet.publicKeyString():
        # if forgerPublicKey != self.wallet.publicKeyString():
            if self.thisBlockValid(listOfForgersPublicKeys) is True:
                if len(listOfForgersPublicKeys) == 1:
                    print(f'I am the next forger, and the block has been verified by {len(listOfForgersPublicKeys)} other node') # make this an f string with how mny it actually is.
                else:
                    print(f'I am the next forger, and the block has been verified by {len(listOfForgersPublicKeys)} other nodes')
                block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)   # SO IT NEEDS TO VERIFY THAT THIS IS THE SAME.
                self.transactionPool.removeFromPool(block.transactions)
                message = Message(self.p2p.socketConnector, 'BLOCK', block)
                encodedMessage = BlockchainUtils.encode(message)
                self.p2p.broadcast(encodedMessage)
            else:
                return self.forge()  # which will work, thankfully.

        elif self.wallet.publicKeyString() in listOfForgersPublicKeys:
            print('I am not the next forger, but I am a validator')
        else:
            print(f'I am not the next forger, it is {forgerPublicKey}')


        ########### so we can see that the forger is always the gensis. I think once i sort that and then validating it with the pthers it will be okay. 






        #if forgerPublicKey == self.wallet.publicKeyString():
        #    blockList = []  # NB could improve optimisation by goin 100, 99, 98 etc. instead of checking all each time. Or just check once. Actually i thin k it might only happen once tbf. 
        #    for forgersPublicKeys in listOfForgersPublicKeys:
#
        #    # need to make this so that is is the forgers shit, not self.
#
        #    # self.blockchain = Blockchain(), self.transactionPool = transactionPool(), self.wallet = Wallet()
#
        #        blockList.append(self.blockchain.createBlock(self.transactionPool.transactions, self.wallet))  # it needs to be the forgers in possibleFprgers self though.
        #    verifiers = 0
        #    block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)
        #    for i in blockList:
        #        if block == blockList[i]: # issue is that this doesnt happen every time maybe?????
        #            verifiers += 1
        #    if verifiers == 100:  # NB this makes the network shut down if there is enough bad nodes.
        #        print('I am the next forger, and have been verified by 100 other nodes')
        #        block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)   # SO IT NEEDS TO VERIFY THAT THIS IS THE SAME.
        #        self.transactionPool.removeFromPool(block.transactions)
        #        message = Message(self.p2p.socketConnector, 'BLOCK', block)
        #        encodedMessage = BlockchainUtils.encode(message)
        #        self.p2p.broadcast(encodedMessage)
        #    else:
        #        return self.forge()
        #elif self.wallet.publicKeyString() in listOfForgersPublicKeys:
        #    print('I am not the next forger, but I am a validator')
        #else:
        #    print('I am not the next forger.')




# currently i have no blockchain, and hence no new nodes get the blockchain/ transcation pool of old because it doesnt exist basicslly. this is because i have no forger .......

#node = Node(1, 5000)
#print(node.forge())

#blockchain = Blockchain()
#blockchain.nextForger()
#blockchain.nextForger()
#pprint.pprint(blockchain.nextForger())
#pprint.pprint(blockchain.possibleForgers)



# current issues: the fucking nodes wont conect atallllllll and there is that error in the node doing the transacation - type error with the list.






    #'''if forger == self.wallet.publicKeyString():
    #    print('i am the next forger')
    #    block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)   # SO IT NEEDS TO VERIFY THAT THIS IS THE SAME.
    #    self.transactionPool.removeFromPool(block.transactions)
    #    message = Message(self.p2p.socketConnector, 'BLOCK', block)
    #    encodedMessage = BlockchainUtils.encode(message)
    #    self.p2p.broadcast(encodedMessage)            
    #else:
    #    print('i am not the next forger')'''

            

#'''def forge(self):
#    forger = self.blockchain.nextForger()  # remember this is more than one of them.
#    if forger == self.wallet.publicKeyString():
#        print('i am the next forger')
#        block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)   # SO IT NEEDS TO VERIFY THAT THIS IS THE SAME.
#        self.transactionPool.removeFromPool(block.transactions)
#        message = Message(self.p2p.socketConnector, 'BLOCK', block)
#        encodedMessage = BlockchainUtils.encode(message)
#        self.p2p.broadcast(encodedMessage)            
#    else:
#        print('i am not the next forger')'''


    #make a functino basicslly saying that it is valid and then out in the andddddddd thing he wrote out. 
