# the initial block in the chain, so the chain has a starting block.
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'trasnsactions': [],
}
# initialize the blockchain list. The genesis block is added to the blockchain for a starting block in the chain.
blockchain = [genesis_block]
# outstanding transactions
open_transactions = []
# global sender for instance of blockchain
owner = 'Chris'


def hash_block(block):
    # creates a hash for the current block and str() is used to stringify the value so it can use the join method.
    return '-'.join([str(block[key]) for key in block])


# returns last blockchain value
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# adds a blockchain value
# sender, recipient, and amount are all basic information of a blockchain transaction instance.
def add_transaction(recipient, sender=owner, amount=1.0):
    """transaction makes a dictionary of sender, recipient, and amount """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)


# mining a block, which confirms the block. takes the open transactions and makes them blocks. Then adds them to the blockchain.
def mine_block():
    # gets the last element in the blockchain.
    last_block = blockchain[-1]
    # hashed_block takes in the hash_block function and stores it in previous_hash to verify it matches the previous block.
    hashed_block = hash_block(last_block)
    # block is a dict because of key, vaule pairs. prev_hash is to help keep blocks in line. Transactions are the blocks sitting in the open_transaction list.
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'trasnsactions': open_transactions,
    }
    # attaches the block to the blockchain
    blockchain.append(block)


# returns user value in a float
def get_trasnsaction_value():
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
    return True


waiting_for_input = True
# while keeps running until it is not true anymore.
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        # tx data gets recipient and sender
        tx_data = get_trasnsaction_value()
        # tuple unpack
        recipient, amount = tx_data
        # amount is hardcoded amount bcause we are skipping the sender parameter in the add_transaction function.
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'trasnsactions': [{'sender': 'Max', 'recipient': 'Chris', 'amount': 100.00}],
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid input. Please try again')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain')
        break
else:
    print('User left!')
print('Done!')
