# initialize the blockchain list
blockchain = []
# outstanding transactions
open_transactions = []
# global sender for instance of blockchain
owner = 'Chris'


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


# mining a block, which confirms the block.
def mine_block():
    pass


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
    # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     if block[0] == blockchain[block_index-1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    return is_valid


waiting_for_input = True
# while keeps running until it is not true anymore.
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain')
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
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
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
