from BlockchainUtils import BlockchainUtils

class Lot:

    def __init__(self, publicKey, iteration, lastBlockHash):
        self.publicKey = str(publicKey)
        self.iteration = iteration
        self.lastBlockHash = str(lastBlockHash)

    def lotHash(self):
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.iteration):
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData
