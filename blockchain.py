# built in library for high order functions
from functools import reduce
# hash library
import hashlib as hl
# json library (imports complex data as strings, use double quotes on key, value)
import json
from collections import OrderedDict


from hash_util import hash_block, hash_string_256

# reward for mining a block. CAPS mean global constant
MINING_REWARD = 10

# the initial block in the chain, so the chain has a starting block.
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
# initialize the blockchain list. The genesis block is added to the blockchain for a starting block in the chain.
blockchain = [genesis_block]
# outstanding transactions
open_transactions = []
# global sender for instance of blockchain
owner = 'Chris'
# all participants. All contained within a set with no duplicate names.
participants = {'Chris'}


def load_data():
    with open('blockchain.txt', mode='r') as f:
        # readlines reads all lines in a list. A list of strings
        file_content = f.readlines()
        # access the global variables
        global blockchain
        global open_transactions
        # file content line one is the blockchain
        blockchain = file_content[0]
        # file content line two is the open transactions. [:-1] removes the \n.
        open_transactions = file_content[1][:-1]


load_data()


def save_data():
    # store blockchains and open_transactions. mode write. Using with helps open and close the function. Cannot write a list, must convert to string.
    with open('blockchain.txt', mode='w') as f:
        f.write(str(blockchain))
        f.write('\n')
        f.write(str(open_transactions))
    # called when saving data or mining a block


def valid_proof(transactions, last_hash, proof):

    # guess is a string of transactions, last_hash, and proof. Then encoded to UTF8. This hash is just for proof, for security.
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # takes the string and makes a hash of it. Hexdigest makes it a valid string(removed when hash util was created.)
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    # fetch last block of current blockchain
    last_block = blockchain[-1]
    # hashes the last block
    last_hash = hash_block(last_block)
    proof = 0
    # used to call valid_proof function. Not is added because guess_hash should have '00' at the beginning.
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    # returns a sum all transaction balances of the participant
    # tx_sender looks at tx['amount'] for each block['transactions'] to see if sender was a participant for each block in the blockchain. already paid.
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    # gets open transactions amounts sent. Trying to pay
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    # adds open transactions amount to sender balance list
    tx_sender.append(open_tx_sender)
    # reduce method which takes a function, sequence(operation), and initial value. Sum() is used to add all items in the list. The return of tx_sum and sum(tx_amount) is returned to tx_sum, then accesses the next amount from tx_sender list. Inline if statement to make sure there is an amount for tx_amount. tx_sum + 0 is used to show  the mining rewards total with the transactions.  If tx_sum wasn't added, mining a block would not reflect the actual sum but sum of all minings.
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # # summing tx['sender'] amount - previous way
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    # returns sum of received amounts
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    # sum of money received. Same method as amount sent.
    amount_received = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # amount_received = 0 (amount received- previous way)
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]
    # total transactions
    return amount_received - amount_sent


def get_last_blockchain_value():
    # returns last blockchain value
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# determining if sender has enough funds to send.


def verify_transaction(transaction):
    # gets the balance of the sender calling the sender on transaction block
    sender_balance = get_balance(transaction['sender'])
    # compares the balance from get_balance to transaction amount. Will return a boolean
    return sender_balance >= transaction['amount']


# adds a blockchain value
# sender, recipient, and amount are all basic information of a blockchain transaction instance.
def add_transaction(recipient, sender=owner, amount=1.0):
    # """transaction makes a dictionary of sender, recipient, and amount """
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }

    # OrderedDict keeps all keys  and values in order so hashes will not change. It takes a list of tuples
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    # checks transaction sender balance against transaction sender amount
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        # adds the sender and recipient to participant set
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


# mining a block, which confirms the block. takes the open transactions and makes them blocks. Then adds them to the blockchain.
def mine_block():
    # gets the last element in the blockchain.
    last_block = blockchain[-1]
    # hashed_block takes in the hash_block function and stores it in previous_hash to verify it matches the previous block.
    hashed_block = hash_block(last_block)
    # proof should not include reward tranaction
    proof = proof_of_work()

    # reward for mining a block transaction - old way
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }

    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

    # copied the whole list of open transactions to append rewards in case there is a problem with open_transactions.
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    # block is a dict because of key, vaule pairs. prev_hash is to help keep blocks in line. Transactions are the blocks sitting in the open_transaction list. The copied_transactions makes it so the block is managed locally, not globally. Proof is added the block to append the proof to the blockchain.
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    # attaches the block to the blockchain
    blockchain.append(block)
    save_data()
    return True


# returns user value in a float
def get_transaction_value():
    # gets dict info for the transactions. sender is a global sender for this instance
    tx_recipient = input('Enter the recipient: ')
    # should be a string identifier
    tx_amount = float(input('Your transaction amount: '))
    # returns a tuple
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


# outputs the entire blockchain
def print_blockchain_elements():
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)


# # the first transaction to the blockchain
# tx_amount = get_trasnsaction_value()
# add_value(tx_amount)


def verify_chain():
    # validates the list of blocks. Checks the hash the old block and stores hashed version in the previous_hash value of the next block. Makes sure every hash match in the block or it will break.
    # wrapping a list in enumerate will returns a tuple, index of element and element itself. Needs to be upacked.
    for (index, block) in enumerate(blockchain):
        # genesis block
        if index == 0:
            continue
        # every block stored has previous_hash
        # compares current block 'previous_hash' with the hash from the hash_block function(previous block).Matching would great, but we are verifying so we are checking to see if they don't match.
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
        # extra step to check the proof to verify chains. Looks at each block transaction. [:-1] removes the reward block from the transaction block
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print("Proof of work is invalid")
            return False
    return True


# With the all method, the funtion verifies all transactions in open_transactions at one time to return a list of booleans. All true make it true. One false render the list false.
def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True
# while keeps running until it is not true anymore.
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants set')
    print('5: Print transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        # tx data gets recipient and sender
        tx_data = get_transaction_value()
        # tuple unpack
        recipient, amount = tx_data
        # amount is hardcoded amount bcause we are skipping the sender parameter in the add_transaction function. We can check true or false because a boolean is returned on the function.
        if add_transaction(recipient, amount=amount):
            print('Added transactions!')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            # resets open_transactions once all blocks are mined.
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Max', 'recipient': 'Chris', 'amount': 100.00}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid input. Please try again')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain')
        break
    # formatting the string so the float is only two spaces.
    print('Balance for {} is ${:6.2f}'.format('Chris', get_balance('Chris')))
else:
    print('User left!')
print('Done!')
