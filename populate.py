import concurrent

from dotenv import load_dotenv
import os
import queue

from database import init_db, insert_transactions
from rpc_handler import get_latest_block_number_json, get_block_data_from_number, get_transaction_data
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var

block_queue = queue.PriorityQueue()
blocks_added = set()

# will store multiple txs at one go. storing one tx at a time is heavy on db
DB_BATCH_SIZE = 20
BLOCK_BATCH_SIZE = 5
THREADS = 3


def fetch_transactions():
    while not block_queue.empty():
        priority, block_data = block_queue.get()
        transactions = block_data["result"]["transactions"]

        block_number = int(block_data["result"]["number"], 16)

        for i in range(0, len(transactions), DB_BATCH_SIZE):
            print("adding {} txs from block: {}".format(min(DB_BATCH_SIZE,len(transactions)), block_number))
            transaction_batch = transactions[i:i+DB_BATCH_SIZE]
            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                futures = [executor.submit(get_transaction_data, tx) for tx in transaction_batch]

                # collect futures, filter out any None which are returned in case of timeout
                tx_raws = [future.result() for future in concurrent.futures.as_completed(futures) if future.result() is not None]
                insert_transactions(tx_raws)


def main():
    while True:
        populate_database()
        fetch_transactions()


# populates db from the latest block that exists to the latest block seen in db
def populate_database():
    init_db()

    latest_block_int = int(get_latest_block_number_json()["result"], 16)

    # add in batches of BLOCK_BATCH_SIZE
    for i in range(latest_block_int, latest_block_int - BLOCK_BATCH_SIZE, -1):
        if i in blocks_added:
            print("block {} seen again, skipping".format(i))
            continue

        block_data = get_block_data_from_number(hex(i))
        print("adding block to queue: {}".format(i))

        # Add the block to the Priority Queue. Use negative block number to process latest blocks first.
        block_queue.put((-i, block_data))
        blocks_added.add(i)

    # print("completed :)")


if __name__ == "__main__":
    main()
