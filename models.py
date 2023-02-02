import sqlite3 as sql
from collections import namedtuple
	
def namedtuple_factory(cursor, row):
  fields = [column[0] for column in cursor.description]
  cls = namedtuple("Row", fields)
  return cls._make(row)

def insertUser(user_id, username, password, timestamp):
	mode = ''
	con = sql.connect("notebookserver.db")
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

def insertCookie(cookie_id, cookie_owner_id, cookie_owner_username, ts, cookie_expire_time, cookie_owner_ts, cookie_owner_last_updated, cookie_expired = False):
	con = sql.connect("notebookserver.db")
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

def verifyCookie():
	cookie = ''
	con = sql.connect('notebookserver.db')
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
	con = sql.connect('notebookserver.db')
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE user_name = :user_name", {"user_name": user_name})
		data = cur.fetchone()
		con.close()
	except Exception as ex:
		data = 'ERROR'
		
	return data

def logout_func(cookie_id):
	con = sql.connect('notebookserver.db')
	try:
		with con:
			cur = con.cursor()
			cur.execute('''SELECT * FROM cookies''')
			cur.execute('''UPDATE cookies SET cookie_expired = :cookie_expired WHERE cookie_id = :cookie_id''', {'cookie_expired': True, 'cookie_id': cookie_id})
	except Exception as ep:
		print(ep)

def retrieveUsers():
	con = sql.connect("notebookserver.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users

def insertFile(file_id, owner_name, data_file, ts):
	res = ''
	try:
		con = sql.connect("notebookserver.db")
		with con:
			cur = con.cursor()
			cur.execute('''INSERT INTO lockedfiles VALUES(
        :file_id,
        :owner_name,
        :data_file,
        :ts,
				:last_updated
      )
      ''',{'file_id': file_id, 'owner_name': owner_name, 'data_file': data_file, 'ts': ts, 'last_updated': ts})
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

def updateFile(file_id, data_file, last_updated):
	res = ''
	try:
		con = sql.connect("notebookserver.db")
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM lockedfiles WHERE file_id = :file_id", {"file_id": file_id})
			cur.execute('''UPDATE lockedfiles SET data_file = :data_file, last_updated = :last_updated WHERE file_id = :file_id''', {'data_file': data_file, 'last_updated': last_updated, 'file_id': file_id})
			con.commit()
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

def retrieveFiles(session_uname):
	con = sql.connect("notebookserver.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM lockedfiles WHERE owner_name = :session_uname", {"session_uname": session_uname})
	docs = cur.fetchall()
	con.close()
	return docs

def retrieveSingleFile(file_id):
	doc = ''
	con = sql.connect('notebookserver.db')
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM lockedfiles WHERE file_id = :file_id", {"file_id": file_id})
		doc = cur.fetchone()
		con.close()
	except Exception as ex:
		doc = ex
	return doc

def deleteFile(file_id):
	res = ''
	try:
		con = sql.connect("notebookserver.db")
		with con:
			cur = con.cursor()
			cur.execute('''SELECT * FROM lockedfiles''')
			cur.execute('''DELETE FROM lockedfiles WHERE file_id = :file_id''', {'file_id': file_id})
			con.commit()
			res = 'okay'
	except Exception as ep:
		res = ep
	return res

def check_key(key_id):
	item = ''
	con = sql.connect('notebookserver.db')
	try:
		con.row_factory = namedtuple_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM keys WHERE key_id = :key_id", {"key_id": key_id})
		item = cur.fetchone()
		con.close()
	except Exception as ex:
		item = ex
	return item
