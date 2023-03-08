import sys
from datetime import datetime
from models import check_key
from models import generate_keys
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
  # Converts a string message to a list of block integers. Each integer
  # represents 128 (or whatever blockSize is set to) string characters.

  messageBytes = message.encode('utf-8') # convert the string to bytes

  blockInts = []
  for blockStart in range(0, len(messageBytes), blockSize):
    # Calculate the block integer for this block of text
    blockInt = 0
    for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
      blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
    blockInts.append(blockInt)
  return blockInts

def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
  # Converts a list of block integers to the original message string.
  # The original message length is needed to properly convert the last
  # block integer.
  message = []
  for blockInt in blockInts:
    blockMessage = []
    for i in range(blockSize - 1, -1, -1):
      if len(message) + i < messageLength:
        # Decode the message string for the 128 (or whatever
        # blockSize is set to) characters from this block integer.
        asciiNumber = blockInt // (BYTE_SIZE ** i)
        blockInt = blockInt % (BYTE_SIZE ** i)
        blockMessage.insert(0, chr(asciiNumber))
    message.extend(blockMessage)
  return ''.join(message)

def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
  # Converts the message string into a list of block integers, and then
  # encrypts each block integer. Pass the PUBLIC key to encrypt.
  encryptedBlocks = []
  n, e = key

  for block in getBlocksFromText(message, blockSize):
    # ciphertext = plaintext ^ e mod n
    encryptedBlocks.append(pow(block, e, n))

  return encryptedBlocks

def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
  # Decrypts a list of encrypted block ints into the original message
  # string. The original message length is required to properly decrypt
  # the last block. Be sure to pass the PRIVATE key to decrypt.
  decryptedBlocks = []
  n, d = key
  for block in encryptedBlocks:
    # plaintext = ciphertext ^ d mod n
    decryptedBlocks.append(pow(block, d, n))
  
  return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)

def readKeyFile(key):
  # Given the filename of a file that contains a public or private key,
  # return the key as a (n,e) or (n,d) tuple value.
  keySize, n, EorD = key.split(',')
  return (int(keySize), int(n), int(EorD))

def decrypt_message(message):
  pk = b'private_key'
  checked_id = check_key(pk)

  if checked_id == None:
    generate_keys()
    checked_id = check_key(pk)
  
  ciphertext = checked_id.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
  )

  return ciphertext

def encrypt_message(message):

  data_file = ""

  def key_pair():
    pk = b'public_key'
    public_bytes = check_key(pk)

    if public_bytes is None:
      generate_keys()
    
    return public_bytes
  
  new_key_pair = key_pair()
  
  # Encrypt the data with the AES session key
  cipher_aes = AES.new(new_key_pair.session_key, AES.MODE_EAX)
  ciphertext, tag = cipher_aes.encrypt_and_digest(message)
  [ data_file(x) for x in (new_key_pair.session_key, cipher_aes.nonce, tag, ciphertext) ]
  
  return