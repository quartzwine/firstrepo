import concurrent

from dotenv import load_dotenv
import os
import time
import queue

from database import init_db, get_latest_stored_block_number, insert_transactions
from main import get_latest_block_number_json, get_block_data_from_number, get_transaction_data, store_transaction
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var

block_queue = queue.PriorityQueue()
blocks_added = set()

# will store multiple txs at one go. storing one tx at a time is heavy on db
BATCH_SIZE = 20


def fetch_transactions():
    while not block_queue.empty():
        priority, block_data = block_queue.get()
        transactions = block_data["result"]["transactions"]

        block_number = int(block_data["result"]["number"],16)

         # lets try this
        for i in range(0, len(transactions), BATCH_SIZE):
            print("adding {} txs from block: {}".format(min(BATCH_SIZE,len(transactions)), block_number))
            transaction_batch = transactions[i:i+BATCH_SIZE]
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(get_transaction_data, tx) for tx in transaction_batch]
                tx_raws = [future.result() for future in concurrent.futures.as_completed(futures)]
                insert_transactions(tx_raws)


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
