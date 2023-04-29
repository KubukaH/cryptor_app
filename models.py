import sqlite3 as sql
from collections import namedtuple
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import timeit
import os

def time_stuff(some_function):
  def wrapper(*args, **kwargs):
    t0 = timeit.default_timer()
    value = some_function(*args, **kwargs)
    # print(timeit.default_timer() - t0, 'seconds')
    return value
  return wrapper

def namedtuple_factory(cursor, row):
  fields = [column[0] for column in cursor.description]
  cls = namedtuple("Row", fields)
  return cls._make(row)

@time_stuff
def insertUser(user_id, username, password, timestamp):
	mode = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		with con:
			cur = con.cursor()
			cur.execute('''INSERT INTO users VALUES(:user_id,:user_name,:password,:ts,:last_updated,:cookie)''',{ 'user_id': user_id, 'user_name': username, 'password': password, 'ts': timestamp, 'last_updated': timestamp, 'cookie': False})
			con.commit()
			del password
			mode = 'success'
	except Exception as ep:
		mode = ep
	
	return mode

@time_stuff
def insertCookie(cookie_id, cookie_owner_id, cookie_owner_username, ts, cookie_expire_time, cookie_owner_ts, cookie_owner_last_updated, cookie_expired = False):
	con = sql.connect(os.path.realpath("notebookserver.db"))
	cur = con.cursor()
	cur.execute(
		'''
		INSERT INTO cookies VALUES(
			:cookie_id, :cookie_owner_id, :cookie_owner_username, :ts, :cookie_expire_time, :cookie_owner_ts, :cookie_owner_last_updated, :cookie_expired
		)
		''', {'cookie_id': cookie_id, 'cookie_owner_id':cookie_owner_id, 'cookie_owner_username':cookie_owner_username, 'ts':ts, 'cookie_expire_time':cookie_expire_time, 'cookie_owner_ts':cookie_owner_ts, 'cookie_owner_last_updated':cookie_owner_last_updated, 'cookie_expired': cookie_expired}
	)
	cur.execute("SELECT * FROM cookies WHERE cookie_expired = :cookie_expired", {"cookie_expired": False})
	cookie = cur.fetchone()
	con.commit()
	con.close()
	return cookie

@time_stuff
def verifyCookie():
	cookie = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM cookies WHERE cookie_expired = :cookie_expired", {"cookie_expired": False})
		cookie = cur.fetchone()
		con.commit()
		con.close()
	except Exception as ep:
		cookie = ep
	return cookie

def searchUser(user_name):
	data = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE user_name = :user_name", {"user_name": user_name})
		data = cur.fetchone()
		con.close()
	except Exception as ex:
		data = "ERROR"
		
	return data

@time_stuff
def logout_func(cookie_id):
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		with con:
			cur = con.cursor()
			cur.execute('''SELECT * FROM cookies''')
			cur.execute('''UPDATE cookies SET cookie_expired = :cookie_expired WHERE cookie_id = :cookie_id''', {'cookie_expired': True, 'cookie_id': cookie_id})
	except Exception as ep:
		print(ep)

@time_stuff
def renew_cookie(cookie_id, cookie_expire_time):
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		with con:
			cur = con.cursor()
			cur.execute('''SELECT * FROM cookies''')
			cur.execute('''UPDATE cookies SET cookie_expire_time = :cookie_expire_time WHERE cookie_id = :cookie_id''', {'cookie_expire_time': cookie_expire_time, 'cookie_id': cookie_id})
	except Exception as ep:
		print(ep)

def retrieveUsers():
	con = sql.connect(os.path.realpath("notebookserver.db"))
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users

@time_stuff
def insertFile(file_id, owner_name, data_file, cipher_aes, tag, session_key, ts):
	res = ''
	try:
		con = sql.connect(os.path.realpath("notebookserver.db"))
		with con:
			cur = con.cursor()
			cur.execute('''INSERT INTO lockedfiles VALUES(
        :file_id,
        :owner_name,
        :data_file,
				:cipher_aes,
				:tag,
				:session_key,
        :ts,
				:last_updated
      )
      ''',{'file_id': file_id, 'owner_name': owner_name, 'data_file': data_file, 'cipher_aes':cipher_aes, 'tag': tag, 'session_key': session_key, 'ts': ts, 'last_updated': ts})
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

@time_stuff
def updateFile(file_id, data_file, tag, cipher_aes, last_updated):
	res = ''
	try:
		con = sql.connect(os.path.realpath("notebookserver.db"))
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM lockedfiles WHERE file_id = :file_id", {"file_id": file_id})
			cur.execute('''
				UPDATE lockedfiles SET 
					data_file = :data_file, 
					tag = :tag,
					cipher_aes = :cipher_aes,
					last_updated = :last_updated
				WHERE file_id = :file_id
			''', 
			{'data_file': data_file, 'tag': tag, 'cipher_aes': cipher_aes, 'last_updated': last_updated, 'file_id': file_id})
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

@time_stuff
def retrieveFiles(session_uname):
	con = sql.connect(os.path.realpath("notebookserver.db"))
	cur = con.cursor()
	cur.execute("SELECT * FROM lockedfiles WHERE owner_name = :session_uname", {"session_uname": session_uname})
	docs = cur.fetchall()
	con.close()
	return docs

@time_stuff
def retrieveSingleFile(file_id):
	doc = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM lockedfiles WHERE file_id = :file_id", {"file_id": file_id})
		doc = cur.fetchone()
		con.close()
	except Exception as ex:
		doc = ex
	return doc

@time_stuff
def deleteFile(file_id):
	res = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		with con:
			cur = con.cursor()
			cur.execute('''SELECT * FROM lockedfiles''')
			cur.execute('''DELETE FROM lockedfiles WHERE file_id = :file_id''', {'file_id': file_id})
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

@time_stuff
def generate_keys():
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		item = ''
		pvt = b'private_key'
		pbl = b'public_key'

		key = RSA.generate(2048)

		public_bytes = key.publickey().export_key()

		private_bytes = key.export_key()
		
		recipient_key = RSA.import_key(public_bytes)
		session_key = get_random_bytes(16)

		# Encrypt the session key with the public RSA key
		cipher_rsa = PKCS1_OAEP.new(recipient_key)
		enc_session_key = cipher_rsa.encrypt(session_key)

		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute('''INSERT INTO keys VALUES(:key_id, :key_data, :session_key)''', {"key_data": public_bytes, "key_id": pbl, "session_key":session_key})
		cur.execute('''INSERT INTO keys VALUES(:key_id, :key_data, :session_key)''', {"key_data": private_bytes, "key_id": pvt, "session_key":enc_session_key})
		con.commit()
		con.close()
	except Exception as ex:
		item = ex
	return item

@time_stuff
def check_key(key_id):
	item = ''
	con = sql.connect(os.path.realpath("notebookserver.db"))
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM keys WHERE key_id = :key_id", {"key_id": key_id})
		item = cur.fetchone()
		con.close()
	except Exception as ex:
		item = ex
	return item
