import concurrent

from dotenv import load_dotenv
import os
import time
import queue

from database import init_db, get_latest_stored_block_number
from main import get_latest_block_number_json, get_block_data_from_number, get_transaction_data, store_transaction
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var

block_queue = queue.PriorityQueue()
blocks_added = set()


def fetch_transactions():
    while not block_queue.empty():
        priority, block_data = block_queue.get()
        transactions = block_data["result"]["transactions"]
    # 8 works ish
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
    while True:  # Run the code inside this loop forever
        populate_database()
        fetch_transactions()
        # time.sleep(2) # base has 2 second block times. should be good for now


# populates sqlite db from the latest block that exists to the latest block seen in db
def populate_database():
    init_db()

    latest_block_int = int(get_latest_block_number_json()["result"], 16)

    # db_latest_block = get_latest_stored_block_number()[0][0]

    # add in batches of 10
    for i in range(latest_block_int, latest_block_int - 10, -1):
        if i in blocks_added:
            print("block {} seen again, skipping".format(i))
            continue

        block_data = get_block_data_from_number(hex(i))
        print("adding block to queue: {}".format(i))
        #print(block_data)

        # Add the block to the Priority Queue. Use negative block number to process latest blocks first.
        block_queue.put((-i, block_data))
        blocks_added.add(i)

    # print("completed :)")


if __name__ == "__main__":
    main()
