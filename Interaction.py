from Wallet import Wallet
from BlockchainUtils import     BlockchainUtils
import requests

def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)


if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    alice.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    postTransaction(exchange, alice, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    
    
    postTransaction(alice, alice, 25, 'STAKE')
    postTransaction(alice, bob, 1, 'TRANSFER')
    postTransaction(alice, bob, 1, 'TRANSFER')
