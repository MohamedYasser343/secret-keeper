import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(key, source, encode=True, keyType='hex', hash_length=216):

    source = source.encode()
    if keyType == 'hex':
        # Convert key (in hex representation) to bytes.
        key = bytes.fromhex(key)

    # Generate a random IV
    IV = os.urandom(AES.block_size)

    # Use AES CBC mode with PKCS7 padding
    cipher = AES.new(key, AES.MODE_CBC, IV)

    # Pad the plaintext to be a multiple of the block size
    padded_data = pad(source, AES.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    # Prepend the IV to the encrypted data
    data_to_hash = IV + encrypted_data

    # Hash the key
    hash_func = hashlib.sha512()
    hash_func.update(key)
    hash_value = hash_func.digest()

    # Truncate the hash to the desired length
    truncated_hash = base64.b64encode(hash_value).decode()[:hash_length]

    # Return Base64 encoded cipher
    return base64.b64encode(data_to_hash).decode() if encode else data_to_hash

def decrypt(key, source, decode=True, keyType='hex', hash_length=216):
    
    source = source.encode()
    if decode:
        source = base64.b64decode(source)

    if keyType == 'hex':
        # Convert key to bytes
        key = bytes.fromhex(key)

    # Extract the IV from the beginning
    IV = source[:AES.block_size]

    # Decrypt the data
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    decrypted_data = decryptor.decrypt(source[AES.block_size:])

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    return unpadded_data.decode()
