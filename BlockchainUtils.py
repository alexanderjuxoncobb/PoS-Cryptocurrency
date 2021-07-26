from Crypto.Hash import SHA256
import json
import jsonpickle


class BlockchainUtils:

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        dataBytes = dataString.encode('utf-8')
        dataHash = SHA256.new(dataBytes)
        return dataHash

    @staticmethod
    def encode(objectToEncode):
        return jsonpickle.encode(objectToEncode)
        # return jsonpickle.encode(objectToEncode, unpickable=True)
    
    @staticmethod
    def decode(encodedObject):
        return jsonpickle.decode(encodedObject)