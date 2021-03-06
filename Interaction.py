from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
from ProofOfStake import ProofOfStake
import json


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

    postTransaction(bob, bob, 25, 'STAKE')
    postTransaction(alice, alice, 25, 'STAKE')
    postTransaction(alice, bob, 1, 'TRANSFER')
    postTransaction(alice, bob, 1, 'TRANSFER')
    postTransaction(bob, bob, 1, 'TRANSFER')
    postTransaction(bob, alice, 1, 'TRANSFER')
    for i in range(1, len(pos.forgers(11234)) - 1):
        if pos.forgers('11234')[0] == pos.forgers('11234')[i]:
            print(f'this is True {i}')
        if pos.forgers('11234')[i-1] == pos.forgers('11234')[i]:
            print(f'this is also true {i}')
        if pos.forgers('11234')[0] != pos.forgers('11234')[i]:
            print(f'false {i}')
        if pos.forgers('11234')[i-1] != pos.forgers('11234')[i]:
            print(f'not true buddy because {pos.forgers(11234)[i-1]} doesnt equal {pos.forgers(11234)[i]} oh and i is {i}')





        #json.dumps(pos.forgers(11234)))


# not mining after the first block ffs. THIS IS THE ISSUE.