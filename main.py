import requests
import json
from dotenv import load_dotenv
import os
import sqlite3

from database import connect, insert_transaction, init_db
from rpc_handler import get_block_data_from_number, get_transaction_data, get_latest_block_number_json


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
        insert_transaction(tx_raw["result"])

        print("-----")


if __name__ == "__main__":
    main()
