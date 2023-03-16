import sqlite3
import time
import random
import string
import os
import timeit
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import os

database_file = os.path.realpath('../files/ohlc.db')

create_statement = 'CREATE TABLE IF NOT EXISTS database_threading_test (symbol TEXT, ts INTEGER, o REAL, h REAL, l REAL, c REAL, vf REAL, vt REAL, PRIMARY KEY(symbol, ts))'
insert_statement = 'INSERT INTO database_threading_test VALUES(?,?,?,?,?,?,?,?)'
select = 'SELECT * from database_threading_test'

def time_stuff(some_function):
    def wrapper(*args, **kwargs):
        t0 = timeit.default_timer()
        value = some_function(*args, **kwargs)
        print(timeit.default_timer() - t0, 'seconds')
        return value
    return wrapper

def generate_values(count=100):
    end = int(time.time()) - int(time.time()) % 900
    symbol = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    ts = list(range(end - count * 900, end, 900))
    for i in range(count):
        yield (symbol, ts[i], random.random() * 1000, random.random() * 1000, random.random() * 1000, random.random() * 1000, random.random() * 1e9, random.random() * 1e5)

def generate_values_list(symbols=1000,count=100):
    values = []
    for _ in range(symbols):
        values.extend(generate_values(count))
    return values

@time_stuff
def sqlite_normal_read():
    """

    100k records in the database, 1000 symbols, 100 rows
    First run
    0.25139795300037804 seconds
    Second run

    Third run
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    try:
        with conn:
            conn.execute(create_statement)
            results = conn.execute(select).fetchall()
            print(len(results))
    except sqlite3.OperationalError as e:
        print(e)

@time_stuff
def sqlite_normal_write():
    """
    1000 symbols, 100 rows
    First run
    2.279409104000024 seconds
    Second run
    2.3364172020001206 seconds
    Third run
    """
    l = generate_values_list()
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    try:
        with conn:
            conn.execute(create_statement)
            conn.executemany(insert_statement, l)

    except sqlite3.OperationalError as e:
        print(e)

@time_stuff
def sequential_batch_read():
    """
    We read all the rows for each symbol one after the other in sequence
    First run
    3.661222331999852 seconds
    Second run
    2.2836898810001003 seconds
    Third run
    0.24514851899994028 seconds
    Fourth run
    0.24082150699996419 seconds
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    try:
        with conn:
            conn.execute(create_statement)
            symbols = conn.execute("SELECT DISTINCT symbol FROM database_threading_test").fetchall()
            for symbol in symbols:
                results = conn.execute("SELECT * FROM database_threading_test WHERE symbol=?", symbol).fetchall()
    except sqlite3.OperationalError as e:
        print(e)  



def sqlite_threaded_read_task(symbol):
    results = []
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    try:
        with conn:
            results = conn.execute("SELECT * FROM database_threading_test WHERE symbol=?", symbol).fetchall()
    except sqlite3.OperationalError as e:
        print(e)
    finally:
        return results

def sqlite_multiprocessed_read_task(symbol):
    results = []
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    try:
        with conn:
            results = conn.execute("SELECT * FROM database_threading_test WHERE symbol=?", symbol).fetchall()
    except sqlite3.OperationalError as e:
        print(e)
    finally:
        return results

@time_stuff
def sqlite_threaded_read():
    """
    1000 symbols, 100 rows per symbol
    First run
    9.429676861000189 seconds
    Second run
    10.18928106400017 seconds
    Third run
    10.382290903000467 seconds
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    symbols = conn.execute("SELECT DISTINCT SYMBOL from database_threading_test").fetchall()
    with ThreadPoolExecutor(max_workers=8) as e:
        results = e.map(sqlite_threaded_read_task, symbols, chunksize=50)
        for result in results:
            pass

@time_stuff
def sqlite_multiprocessed_read():
    """
    1000 symbols, 100 rows
    First run
    0.2484774920012569 seconds!!!
    Second run
    0.24322178500005975 seconds
    Third run
    0.2863524549993599 seconds
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    symbols = conn.execute("SELECT DISTINCT SYMBOL from database_threading_test").fetchall()
    with ProcessPoolExecutor(max_workers=8) as e:
        results = e.map(sqlite_multiprocessed_read_task, symbols, chunksize=50)
        for result in results:
            pass

def sqlite_threaded_write_task(n):
    """
    We ignore the database locked errors here. Ideal case would be to retry but there is no point writing code for that if it takes longer than a sequential write even without database locke errors
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    data = list(generate_values())
    try:
        with conn:
            conn.executemany("INSERT INTO database_threading_test VALUES(?,?,?,?,?,?,?,?)",data)
    except sqlite3.OperationalError as e:
        print("Database locked",e)
    finally:
        conn.close()
        return len(data)

def sqlite_multiprocessed_write_task(n):
    """
    We ignore the database locked errors here. Ideal case would be to retry but there is no point writing code for that if it takes longer than a sequential write even without database locke errors
    """
    conn = sqlite3.connect(os.path.realpath('../files/ohlc.db'))
    data = list(generate_values())
    try:
        with conn:
            conn.executemany("INSERT INTO database_threading_test VALUES(?,?,?,?,?,?,?,?)",data)
    except sqlite3.OperationalError as e:
        print("Database locked",e)
    finally:
        conn.close()
        return len(data)

@time_stuff
def sqlite_threaded_write():
    """

    Did not write all the results but the outcome with 97400 rows written is still this...
    Takes 20x the amount of time as a normal write
    1000 symbols, 100 rows
    First run
    28.17819765000013 seconds
    Second run
    25.557972323000058 seconds
    Third run
    """
    symbols = [i for i in range(1000)]
    with ThreadPoolExecutor(max_workers=8) as e:
        results = e.map(sqlite_threaded_write_task, symbols, chunksize=50)
        for result in results:
            pass

@time_stuff
def sqlite_multiprocessed_write():
    """
    1000 symbols, 100 rows
    First run
    30.09209805699993 seconds
    Second run
    27.502465319000066 seconds
    Third run
    """
    symbols = [i for i in range(1000)]
    with ProcessPoolExecutor(max_workers=8) as e:
        results = e.map(sqlite_multiprocessed_write_task, symbols, chunksize=50)
        for result in results:
            pass


sqlite_normal_write()