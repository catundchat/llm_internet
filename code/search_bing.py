# -*- coding: utf-8 -*-
from pprint import pprint
import requests

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = 'YOUR-AZURE-BING-API-KEY'
endpoint = 'YOUR-ENDPOINT'

# Query term(s) to search for. 
query = "谈谈最近的巴以冲突"

# Construct a request
mkt = 'zh-CN'  # Chinese market
params = { 'q': query, 'mkt': mkt }
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
try:
    response = requests.get(endpoint + "/v7.0/search", headers=headers, params=params)
    response.raise_for_status()

    print("Headers:")
    print(response.headers)

    print("\nJSON Response:")
    pprint(response.json())
except Exception as ex:
    raise ex