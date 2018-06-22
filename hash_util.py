import hashlib as hl
import json


# hash string function to clean code on blockchain.py
def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    # creates a hash for the current block and str() is used to stringify the value so it can use the join method.
    # return '-'.join([str(block[key]) for key in block]) - old  hash

    # hashlib hashes the block so it is unreadable unless you have the hash table.  sha256 creates a 64 character hash. The hash should be a string still. Cannot turn objects to json. JSON.dumps takes the block, which is a dict, and turns it into a string. encode is called to re-encode to UTF8 as a binary string. Hexdigest is  used to translate sha256 binary string to normal characters. Now hash block contains all of the block's information, including previous_hash, to check if hashes match. Sort_keys leads same dict to same string.

    # hashble block is used to make the block, created from Block class, into a dictionary which can be hashed. Using copy so it doesn't overide other blocks. New dict, new block
    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
