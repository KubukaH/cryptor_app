from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from tkinter.messagebox import showerror, showinfo
from models import check_key, generate_keys
import secrets
from datetime import datetime
from models import insertFile, updateFile, retrieveSingleFile
import generate_secrets

def lock_file(session_cookie, upd_id, text_message, mode):
  res = None

  if len(text_message) > 5:
    pk = b'public_key'

    new_key_pair = check_key(pk)

    if new_key_pair is None:
      item = generate_keys()
      showinfo(item)
      new_key_pair = check_key(pk)
    else:
      new_key_pair = check_key(pk)
    
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(new_key_pair.session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(text_message.encode("utf-8"))

    if mode == 'create':
      response = insertFile(file_id=generate_secrets.hashed_id(secrets.token_bytes(24)), owner_name=session_cookie[2], data_file=ciphertext, cipher_aes=cipher_aes.nonce, tag=tag, session_key=new_key_pair.session_key, ts=datetime.now())
      res = response

    if mode == 'update':
      response = updateFile(
        file_id=upd_id.get().encode('utf-8'), 
        data_file=ciphertext,
        tag=tag,
        cipher_aes=cipher_aes.nonce,
        last_updated=datetime.now()
      )
      res = response

  else:
    res = 'The text editor is blank or the characters are less than the required minimum number. Type something first to continue.'

  return res

# MODE DECRYPT MESSAGE
def decrypt(doc_id):
  msg = ''
  if len(doc_id.get()) > 1:
    docfile = retrieveSingleFile(doc_id.get().encode('utf-8'))

    if docfile != None:
      bytes_k = check_key('private_key'.encode("utf-8"))
      private_key = RSA.import_key(bytes_k[1])

      # Decrypt Session Key
      cipher_rsa = PKCS1_OAEP.new(private_key)
      session_key = cipher_rsa.decrypt(bytes_k[2])

      # Decrypt the data with the AES session key
      cipher_aes = AES.new(session_key, AES.MODE_EAX, docfile[3])
      msg = cipher_aes.decrypt_and_verify(docfile[2], docfile[4])

    else:
      showerror("Empty Document")
  else:
    showerror("Can't perform search.")

  return msg
