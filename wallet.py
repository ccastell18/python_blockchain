from Crypto.PublicKey import RSA
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

    def load_keys(self):
        pass

    def generate_keys(self):
        # higher the number, more secure.  Higher also means more time to generate. Keys are made in binary format, need to return in string form.
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        # use hexlify for the hexidecimal representation of binascii. export the key and format DER is binary key unencrypted. decode with ascii to covert to acii characters.
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))
