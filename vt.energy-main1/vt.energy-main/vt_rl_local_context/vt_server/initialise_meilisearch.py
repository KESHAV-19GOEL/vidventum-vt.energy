import os
import json
import requests
from vt_run.config.server_config import VT_SANIC_SETUP

VT_MEILI_URL = VT_SANIC_SETUP['VT_MEILI_URL']
VT_INDEX_NAME = VT_SANIC_SETUP['VT_INDEX_NAME']
VT_Documents_File = VT_SANIC_SETUP['VT_Documents_File']
VT_SCHEMA_FILE = VT_SANIC_SETUP['VT_SCHEMA_FILE']


def load_documents():
    if os.path.exists(VT_Documents_File):
        with open(VT_Documents_File, 'r') as file:
            return json.load(file)
    return []

# Save documents to a file
def save_documents(documents):
    with open(VT_Documents_File, 'w') as file:
        json.dump(documents, file, indent=4)

# Function to dynamically collect documents
def get_documents():
    documents = load_documents()
    print("Loaded existing documents:")
    for doc in documents:
        print(doc)

    while True:
        doc_id = input("Enter document ID (or 'done' to finish): ")
        if doc_id.lower() == 'done':
            break
        BusinessName = input("Enter document business name: ")
        description = input("Enter document description: ")
        documents.append({
            "id": int(doc_id),
            "businessName": BusinessName,
            "description": description
        })
    
    save_documents(documents)
    return documents

# Main process to add documents to MeiliSearch
def initialize_meilisearch():
    # Create an index if it doesn't exist
    response = requests.post(f'{VT_MEILI_URL}/indexes', json={"uid": VT_INDEX_NAME})
    if response.status_code == 200:
        print("Index created successfully.")
    else:
        print(f"Index creation response: {response.json()}")

    # Get documents from user input
    documents = get_documents()

    # Add documents to the index
    response = requests.post(f'{VT_MEILI_URL}/indexes/{VT_INDEX_NAME}/documents', json=documents)
    print(response.json())

if __name__ == '__main__':
 initialize_meilisearch()
