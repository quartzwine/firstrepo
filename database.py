import sqlite3


def connect():
    conn = sqlite3.connect('transactions.db')
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', create_entry_from_transaction(transaction))
    conn.commit()
    conn.close()


# this needs to line up with table schema. if second parameter is not empty string it is required.
def create_entry_from_transaction(transaction) :
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
