import binascii
from dataclasses import dataclass
import base58
import codecs
import hashlib

from ecdsa import NIST256p, SigningKey

import utils


class Wallet(object):
    def __init__(self) -> None:
        self.__private_key = SigningKey.generate(curve=NIST256p)
        self.__public_key = self.__private_key.get_verifying_key()
        self.__blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self.__private_key.to_string().hex()

    @property
    def public_key(self):
        return self.__public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self.__blockchain_address

    def generate_blockchain_address(self):
        sha256_bpk = hashlib.sha256(self.__public_key.to_string())
        sha256_bpk_digest = sha256_bpk.digest()

        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk.digest(), 'hex')

        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')

        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_2_nbpk = hashlib.sha256(sha256_bpk.digest())
        sha256_hex = codecs.encode(sha256_2_nbpk.digest(), 'hex')

        checksum = sha256_hex[:8]
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        blockchain_address = base58.b58encode(
            binascii.unhexlify(address_hex)).decode('utf-8')
        return blockchain_address


@dataclass
class Transaction(object):
    sender_private_key: str
    sender_public_key: str
    sender_blockchain_address: str
    recipient_blockchain_address: str
    value: float

    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': self.sender_blockchain_address,
            'recipient_blockchain_address': self.recipient_blockchain_address,
            'value': float(self.value)
        })
        print(str(transaction))
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p)
        private_key_sign = private_key.sign(message)
        sigunature = private_key_sign.hex()
        return sigunature


if __name__ == '__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)
    print(wallet.blockchain_address)
