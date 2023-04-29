from hashlib import blake2b
from hmac import compare_digest

#HASHLIB SIGNATURE MAKING
def hash_sign(cookie, secret):
  h = blake2b(digest_size=32, key=secret)
  h.update(cookie)
  return h.hexdigest().encode('utf-8')

def verify(cookie, sig, secret):
  good_sig = hash_sign(cookie, secret)
  return compare_digest(good_sig, sig)

def hashed_id(pid):
  h = blake2b(digest_size=24)
  h.update(pid)
  return h.hexdigest().encode('utf-8')