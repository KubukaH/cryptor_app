import sqlite3

def run_connection():
  init_connection = sqlite3.connect('notebookserver.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
  cur = init_connection.cursor()
  cur.executescript('''
    BEGIN;
    CREATE TABLE IF NOT EXISTS lockedfiles(
      file_id PRIMARY KEY UNIQUE,
      owner_name TEXT,
      data_file TEXT,
      cipher_aes TEXT,
      tag TEXT,
      session_key TEXT,
      ts TIMESTAMP,
      last_updated TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS users(
      user_id PRIMARY KEY UNIQUE,
      user_name TEXT UNIQUE,
      password TEXT,
      ts timestamp,
      last_updated DATE,
      cookie BOOLEAN
    );
    CREATE TABLE IF NOT EXISTS cookies(
      cookie_id PRIMARY KEY UNIQUE, 
      cookie_owner_id TEXT, 
      cookie_owner_username TEXT, 
      ts TIMESTAMP, 
      cookie_expire_time DATE,
      cookie_owner_ts TIMESTAMP,
      cookie_owner_last_updated DATE,
      cookie_expired BOOLEAN
    );
    CREATE TABLE IF NOT EXISTS keys(
      key_id PRIMARY KEY UNIQUE,
      key_data TEXT,
      session_key TEXT
    );
    COMMIT;
  ''')