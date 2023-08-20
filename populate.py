import concurrent

from dotenv import load_dotenv
import os

from database import init_db, get_latest_stored_block_number
from main import get_latest_block_number_json, get_block_data_from_number, get_transaction_data, store_transaction
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var


def fetch_transactions(transactions):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_transaction_data, tx) for tx in transactions]
        for future in concurrent.futures.as_completed(futures):
            try:
                tx_raw = future.result()
                print("storing tx hash: {}".format(tx_raw["result"]["hash"]))
                store_transaction(tx_raw["result"])
            except Exception as e:
                print(f"An error occurred: {e}")
                print(tx_raw)


def main():
    populate_database()


# populates sqlite db from the latest block seen in db to latest block that exists
def populate_database():
    init_db()

    latest_block_int = int(get_latest_block_number_json()["result"], 16)  # from json hex string to int
    db_latest_block = get_latest_stored_block_number()[0][0]  # db returns list of tuple

    for i in range(db_latest_block+1, latest_block_int):
        block_data = get_block_data_from_number(hex(i))
        print("populating block: {}".format(i))
        print(block_data)
        fetch_transactions(block_data["result"]["transactions"])

        print("completed :)")


if __name__ == "__main__":
    main()