from Lot import Lot
from BlockchainUtils import BlockchainUtils
import random

# need to make sure he gets validated.


class ProofOfStake:

    def __init__(self):
        self.stakers = {}
        self.setGenesisNodeStake()
        
    def setGenesisNodeStake(self):
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        self.stakers[genesisPublicKey] = 1


    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake
        else:
            self.stakers[publicKeyString] = stake

    def get(self, publicKeyString):
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None

    def validatorLots(self, seed):
        # PUT INTO RANDOM LIST. PICK RANDOM NUMBERS. CHOOSE 100 FROM IT, 1 OF THEM GETS NEXT BLOCK AND 100 ARE RECHOSEN.
        lots = []
        for validator in self.stakers.keys(): #issue i believe is that only! the intiial key is a staker - FINE NOW
            for stake in range(self.get(validator)):  # this is where we get the staking aspect 
                lots.append(Lot(validator, stake+1, seed))   # +1 is so that you dont have a lot of 0 stake.  if not, then woul be the same each time and a higher stake != better chance of being nect forger. 
        random_lots = []
        if len(lots) >= 100:
            for _ in range(100):
                random_lots.append(random.choice(lots))
        else:
            for _ in range(len(lots)):
                random_lots.append(random.choice(lots))
        return random_lots  # these are the lots which contain our next validator.

    def winnerLot(self, random_lots, seed):  # Seed is the last block hash
        winnerLot = None
        leastOffset = None
        referenceHashIntValue = int(BlockchainUtils.hash(seed).hexdigest(), 16)
        for lot in random_lots:
            lotIntValue = int(lot.lotHash(), 16)
            offset = abs(lotIntValue - referenceHashIntValue)
            if leastOffset is None or offset < leastOffset:
                leastOffset = offset
                winnerLot = lot
        return winnerLot

    def forgers(self, lastBlockHash):    # still havent made it from the last 100. need to try and do that. 
        random_lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(random_lots, lastBlockHash)
        listOfLots = [winnerLot.publicKey]  # so, the winner lot is in position 0.
        for lot in random_lots:
            #if lot != winnerLot:
            listOfLots.append(lot.publicKey)
        return listOfLots   # maybe the key is to have the dictionary here. then when you find the actual transaction we check that it's valid witb all of them???????

    def forger(self, lastBlockHash):
        return self.forgers(lastBlockHash)[0]





# NOW NEED TO MAKE SURE: VALIDATORS VALIDATE, IT IS ONLY SLECTED FROM THE STAKERS- SO IF YOU UPDATE THEY GET ADDED TO THE STAKING POOL. HOW TO GET BOB TO DO IT YEAH?????

    

    #def validators(self):
    #    random_lots = self.random_lots
    #    RandomLotsPublicKeys = []
    #    for lots in random_lots:
    #        RandomLotsPublicKeys.append(lots.publicKey)
    #    return RandomLotsPublicKeys  # so it is a list




        # Now i need the other 99 to validate the block..... !!!!!!!!!!!






#pos but limited to 5% of network 
