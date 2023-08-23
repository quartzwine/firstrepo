import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_PASS = os.getenv('DB_PASS')


def connect():
    # modify this to your own taste
    conn = psycopg2.connect(
        dbname="blockchain",
        user="postgres",
        password=DB_PASS,
        host="localhost",
        port="5432"
    )
    return conn


def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            blockHash        TEXT NOT NULL,
            blockNumber      INTEGER NOT NULL,
            from_address     TEXT NOT NULL,
            gas              TEXT NOT NULL,
            gasPrice         TEXT NOT NULL,
            hash             TEXT NOT NULL,
            input            TEXT,
            nonce            TEXT NOT NULL,
            to_address       TEXT,
            transactionIndex INTEGER NOT NULL,
            value            TEXT NOT NULL,
            type             TEXT,
            v                TEXT,
            r                TEXT,
            s                TEXT,
            sourceHash       TEXT,
            mint             TEXT,
            PRIMARY KEY (hash)
        );
    ''')
    conn.commit()
    conn.close()


def insert_transaction(transaction):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (blockHash, blockNumber, from_address, gas, gasPrice, hash, input, nonce, to_address, transactionIndex, value, type, v, r, s, sourceHash, mint)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', create_entry_from_transaction(transaction))
    conn.commit()
    conn.close()


def insert_transactions(tx_raws):
    transactions = [tx_raw["result"] for tx_raw in tx_raws]
    conn = connect()
    cursor = conn.cursor()
    query = '''
        INSERT INTO transactions (blockHash, blockNumber, from_address, gas, gasPrice, hash, input, nonce, to_address, transactionIndex, value, type, v, r, s, sourceHash, mint)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = [create_entry_from_transaction(transaction) for transaction in transactions]
    cursor.executemany(query, data)
    conn.commit()
    conn.close()


# this needs to line up with table schema. if second parameter is not empty string it is required.
def create_entry_from_transaction(transaction):
    return (
        transaction.get('blockHash', ''),
        int(transaction.get('blockNumber', '0'), 16),
        transaction.get('from', ''),
        transaction.get('gas', ''),
        transaction.get('gasPrice', ''),
        transaction.get('hash', ''),
        transaction.get('input', ''),
        transaction.get('nonce', ''),
        transaction.get('to', ''),
        int(transaction.get('transactionIndex', '0'), 16),
        transaction.get('value', ''),
        transaction.get('type', ''),
        transaction.get('v', ''),
        transaction.get('r', ''),
        transaction.get('s', ''),
        transaction.get('sourceHash', ''),
        transaction.get('mint', '')
    )


def get_all_transactions():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions


def get_latest_stored_block_number():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(blockNumber) from transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions
