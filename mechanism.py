import sys
from datetime import datetime
from models import check_key

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
  r_msg = ''
  checked_id = check_key("private_key")

  keySize = int(checked_id[1])
  n = int(checked_id[2])
  d = int(checked_id[3])

  # Read in the message length and the encrypted message from the file.
  messageLength, blockSize, encryptedMessage = message[2].split('_')
  messageLength = int(messageLength)
  blockSize = int(blockSize)
  # Check that key size is greater than block size.
  if keySize < blockSize * 8:
    sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))

  # Convert the encrypted message into large int values.
  encryptedBlocks = []
  for block in encryptedMessage.split(','):
    encryptedBlocks.append(int(block))
      
  r_msg = decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)

  return r_msg

def encrypt_message(message):
  r_msg = ''
  checked_id = check_key("public_key")

  blockSize=DEFAULT_BLOCK_SIZE
  keySize = int(checked_id[1])
  n = int(checked_id[2])
  e = int(checked_id[3])

  if keySize < blockSize * 8: # * 8 to convert bytes to bits
    sys.exit('ERROR: Block size is {0} bits and key size is {1} bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?'.format(blockSize * 8, keySize))

  encryptedBlocks = encryptMessage(message, (n, e), blockSize)

  for i in range(len(encryptedBlocks)):
    encryptedBlocks[i] = str(encryptedBlocks[i])
  encryptedContent = ','.join(encryptedBlocks)

  r_msg = '{0}_{1}_{2}'.format(len(message), blockSize, encryptedContent)

  return r_msg