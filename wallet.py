from Crypto.PublicKey import RSA
# generates signatures
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
# can convert binary to ascii and ascii to binary
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        try:
            with open('wallet.txt', mode='w') as f:
                f.write(public_key)
                f.write('\n')
                f.write(private_key)
        except(IOError, IndexError):
            print('Saving wallet failed...')

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                # return a list of strings
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except (IOError, IndexError):
            print('Loading wallet failed')

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except(IOError, IndexError):
                print('Saving wallet failed...')

    def generate_keys(self):
        # higher the number, more secure.  Higher also means more time to generate. Keys are made in binary format, need to return in string form.
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        # use hexlify for the hexidecimal representation of binascii. export the key and format DER is binary key unencrypted. decode with ascii to covert to acii characters.
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        # keys are stored as strings, must convert to binary
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        # hash or payload
        h = SHA256.new((str(sender) + str(recipient) +
                        str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')
