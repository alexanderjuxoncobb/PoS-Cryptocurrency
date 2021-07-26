from BlockchainUtils import BlockchainUtils
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=apiPort)

    def injectNode(self, injectedNode):
        global node
        node = injectedNode

    @route('/info', methods=['GET'])
    def info(self):
        return "this is a communication interface to a node's blockchain", 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200

    @route('transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
