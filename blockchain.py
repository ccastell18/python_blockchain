# initialize the blockchain list
blockchain = []


# returns last blockchain value
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# adds a blockchain value
def add_value(transaction_amount, last_transaction=[1]):
    """appends new value to blockchain
      transaction_amount-the amount to be added
      last_transaction-last blockchain value(default 1)
      """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


# returns user value in a float
def get_trasnsaction_value():
    user_input = float(input('Your transaction: '))
    return user_input


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


# outputs the entire blockchain
def print_blockchain_elements():
    for block in blockchain:
        print('Outputting block')
        print(block)


# # the first transaction to the blockchain
# tx_amount = get_trasnsaction_value()
# add_value(tx_amount)


def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        if block[0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid


# while keeps running until it is not true anymore.
while True:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_trasnsaction_value()
        add_value(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        break
    else:
        print('Invalid input. Please try again')
    if not verify_chain():
        print('Invalid blockchain')
        break
print('Done!')
