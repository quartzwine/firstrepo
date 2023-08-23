import json
import requests
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var


# TODO: cant add this to any other functions. breaks with duplicate key error need to look closer
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_post_request(payload: str) -> dict:
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    return json.loads(response.text)


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
    return send_post_request(payload)


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

