"""Provides API Handlers for MeiliSearch 

#==========================LICENSE NOTICE==========================
#
# Copyright (c) 2024 Vidcentum Technologies Pvt Ltd, India.
# License: Refer to LICENSE file of the software package.
# Email: support@vidcentum.com
# Website: https://vidcentum.com
#
##=======================END LICENSE NOTICE========================
"""
import requests
import json 
import os

# Create an index
index_name = "business_data"
requests.post(f'http://127.0.0.1:7700/indexes/{index_name}')

# Load documents from the documents.json file
json_file_path = os.path.join(os.path.dirname(__file__),'documents.json')
with open(json_file_path,'r') as file:
    documents = json.load(file)

# Add documents to the index
response = requests.post(f'http://127.0.0.1:7700/indexes/{index_name}/documents', json=documents)
print(response.json())

# Perform a search query to verify documents
search_query = {"q": "Example"}
response = requests.post(f'http://127.0.0.1:7700/indexes/{index_name}/search', json=search_query)
print("Search query response:", response.json())