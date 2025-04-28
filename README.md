This project implements a blockchain using a validator lottery-based Proof of Stake (PoS) consensus mechanism that I designed. It was developed as part of my UROP at Imperial College London.

## Core Components

- **Wallet**: Manages keypairs, creates and signs transactions and blocks
- **Block/Blockchain**: Maintains the chain of blocks and validates transactions
- **ProofOfStake**: Implements the custom PoS algorithm for selecting block forgers
- **Node**: Handles P2P communication, transaction processing, and block forging
- **Transaction/TransactionPool**: Handles the creation and temporary storage of transactions

## Novel PoS Features

- **Validator Lottery with Weighted Selection**: Rather than selecting validators purely by stake percentage, the system creates "lottery tickets" (lots) proportional to stake size, then randomly selects 100 validators from this pool, preserving proportionality while introducing randomness.
- **Hash-Proximity Selection**: The winner is determined by calculating the mathematical distance between each validator's lot hash and the reference hash derived from the previous block. The validator with the smallest offset wins the right to forge.
- **Two-Tier Validation**: The system implements a consensus layer where the top validator must have their block verified by other validators before it's accepted, providing resistance against forged blocks.  
- **Stake Proportional but Non-Deterministic**: Unlike pure deterministic selection methods, this approach maintains proportional representation while introducing entropy into the selection process. This randomness forces attackers to spread their resources thin across multiple potential targets rather than concentrating on a known validator, making the attack less efficient and more costly to execute.
- **Optimized for Multi-Validator Verification**: The system specifically creates not just a single forger but a prioritized list of 100 validators that participate in block verification, enhancing security and decentralization.

## Key Features

- Distributed P2P network with automatic peer discovery
- REST API for interacting with nodes
- Support for multiple transaction types (EXCHANGE, TRANSFER, STAKE)
- Genesis node bootstrapping for network initialization

The system is designed to balance security, decentralization, and efficiency while being resistant to common attack vectors in consensus mechanisms.
