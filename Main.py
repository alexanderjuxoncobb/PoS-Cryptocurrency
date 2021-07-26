from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
import pprint
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys

# /usr/bin/python3 

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyFile = None
    if len(sys.argv)>4:
        keyFile = sys.argv[4]

    node = Node(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)
