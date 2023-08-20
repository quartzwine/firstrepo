import requests
import json
from dotenv import load_dotenv
import os
import sqlite3

from database import connect, insert_transaction, init_db

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var


def main():

    # initialize database
    init_db()

    block_number_json = get_latest_block_number_json()
    print(block_number_json)
    print("blocks")

    block_data = get_block_data_from_number(block_number_json["result"])

    # print out all Txs in block
    for tx in block_data["result"]["transactions"]:
        print("Data for {}".format(tx))
        tx_raw = get_transaction_data(tx)
        store_transaction(tx_raw["result"])

        print("-----")


def store_transaction(transaction):
    insert_transaction(transaction)


# returns a json
def get_block_data_from_number(block_number) -> dict:
    payload = json.dumps({
        "method": "eth_getBlockByNumber",
        "params": [
            block_number,
            False
        ],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    return response_json


def get_latest_block_number_json() -> dict:
    payload = json.dumps({
      "method": "eth_blockNumber",
      "params": [],
      "id": 1,
      "jsonrpc": "2.0"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    return response_json


def print_transaction_data(tx):
    payload = json.dumps({
        "method": "eth_getTransactionByHash",
        "params": [
            tx
        ],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    print(response.text)


def get_transaction_data(tx):
    payload = json.dumps({
        "method": "eth_getTransactionByHash",
        "params": [
            tx
        ],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    return response_json


if __name__ == "__main__":
    main()