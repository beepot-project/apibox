import json
import os
import warnings
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_account._utils.structured_data.hashing import (
hash_domain,
hash_message as hash_eip712_message,
load_and_validate_structured_message,
)
from eth_account._utils.validation import (
is_valid_address,
)
from collections.abc import (
Mapping,
)

from cytoolz import (
    dissoc,
)
from eth_keyfile import (
    create_keyfile_json,
    decode_keyfile_json,
)
from eth_keys import (
    KeyAPI,
    keys,
)
from eth_keys.exceptions import (
    ValidationError,
)
from eth_utils.curried import (
    combomethod,
    hexstr_if_str,
    is_dict,
    keccak,
    text_if_str,
    to_bytes,
    to_int,
)
from hexbytes import (
    HexBytes,
)

from eth_account._utils.legacy_transactions import (
    Transaction,
    vrs_from,
)
from eth_account._utils.signing import (
    hash_of_signed_transaction,
    sign_message_hash,
    sign_transaction_dict,
    to_standard_signature_bytes,
    to_standard_v,
)
from eth_account._utils.typed_transactions import (
    TypedTransaction,
)
from eth_account.datastructures import (
    SignedMessage,
    SignedTransaction,
)
from eth_account.hdaccount import (
    ETHEREUM_DEFAULT_PATH,
    generate_mnemonic,
    key_from_seed,
    seed_from_mnemonic,
)
from eth_account.messages import (
    SignableMessage,
    _hash_eip191_message,
)
from eth_account.signers.local import (
    LocalAccount,
)
from typing import (
NewType,
TypeVar,
Union,
)
from common.dataformat import logger
def signMessage(message, privkey):
    logger.info("\n \nFunction signMessage(message, privkey)")
    encode_message = encode_defunct(text = message)
    logger.info("plaintext:")
    logger.info(encode_message.body)
    signer = w3.eth.account.sign_message(encode_message, privkey)

    logger.info("signed hash hex:")
    logger.info(signer.signature.hex())
    account = w3.eth.account.from_key(privkey)
    
    logger.info("author address:")
    logger.info(account.address)
    return signer.signature.hex(), account.address

def getEccUser(privkey):
    logger.info("\n \nFunction getEccUser(privkey)")
    account = w3.eth.account.from_key(privkey)
    logger.info("user address: ")
    logger.info(account.address)
    return account.address

def getEccPubkey(privkey):
    logger.info("\n \nFunction getEccPubkey(privkey)")
    account = w3.eth.account.from_key(privkey)
    logger.info("user pubkey: ")
    logger.info(account._key_obj.public_key)
    return account._key_obj.public_key

def getEccHdUser(mnemonic, path):
    from eth_account import Account
    Account.enable_unaudited_hdwallet_features()
    logger.info("\n \nFunction getEccHdUser(mnemonic, path)")
    #w3.eth.account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(mnemonic, "", path)
    logger.info("user address: ")
    logger.info(account.address)
    logger.info("HD user path: ")
    logger.info(path)
    privateKey = account._key_obj.to_hex().replace("0x", "")
    return account.address,privateKey

def getEcdhShareKey(privkey_hex, pubkey_hex):
    logger.info("\n \nFunction getEcdhShareKey(privkey_hex, pubkey_hex)")
    import ecdsa
    from ecdsa.curves import (
     SECP256k1   
    )
    from ecdsa.keys import SigningKey, VerifyingKey
    privkey = SigningKey.from_string(bytearray.fromhex(privkey_hex), SECP256k1)
    pubkey = VerifyingKey.from_string(bytearray.fromhex(pubkey_hex), SECP256k1)
    import ecdsa.ecdh
    
    share_key = ecdsa.ecdh.ECDH(SECP256k1, privkey, pubkey)
    return share_key.generate_sharedsecret_bytes().hex()

def aesEnCrypto(key, plaintext):
    logger.info("\n \nFunction aesEnCrypto(key, plaintext)")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    bkey = bytes(key, 'utf-8') 
    iv = b"1234567890123456"
    cipher = AES.new(bkey, AES.MODE_CBC, iv)
    bplainttext =bytes(plaintext, 'utf-8')
    ct_bytes  = cipher.encrypt(pad(bplainttext, AES.block_size))
    return ct_bytes.hex()

def aesDeCrypto(key, plaintext):
    logger.info("\n \nFunction aesDeCrypto(key, plaintext)")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from base64 import b64encode
    bkey = bytes(key, 'utf-8') 
    iv = b"1234567890123456"
    cipher = AES.new(bkey, AES.MODE_CBC, iv)
    bplainttext =bytes(plaintext, 'utf-8')
    ct_bytes  = cipher.encrypt(pad(bplainttext, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    print(ct_bytes.hex())