from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
from ProofOfStake import ProofOfStake

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

    pos = ProofOfStake()
    #pos.update(bob.publicKeyString(), 100)
    pos.update(bob.publicKeyString(), 100)

    postTransaction(exchange, alice, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    # postTransaction(exchange, bob, 100, 'EXCHANGE')
    print(f'BOOOOOOOOOOOOB = {bob.publicKeyString()}')    # NB so nodes and stakers can be seperate.

    #postTransaction(alice, alice, 25, 'STAKE')
    postTransaction(bob, bob, 25, 'STAKE')
    postTransaction(alice, bob, 1, 'TRANSFER')
    postTransaction(alice, bob, 1, 'TRANSFER')