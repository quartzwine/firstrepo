import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

env_var = os.getenv('API_KEY')
url = "https://tiniest-little-meme.base-mainnet.discover.quiknode.pro/" + env_var

payload = json.dumps({
  "method": "eth_getBlockByNumber",
  "params": [
    hex(2949985),
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
print(response.text)
