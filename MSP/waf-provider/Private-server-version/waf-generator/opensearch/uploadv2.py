import json
import os
from typing import Dict, Any, List
from opensearchpy import OpenSearch, RequestsHttpConnection, helpers
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain.docstore.document import Document
from tqdm.auto import tqdm
import time
from langchain.text_splitter import CharacterTextSplitter

AZURE_OPENAI_EMBEDDING_KEY = "text-embedding-3-small"
os.environ["AZURE_OPENAI_API_KEY"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = ""

# Set up Azure OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDING_KEY,
    openai_api_version="2023-05-15",
)

# OpenSearch client
host = ""  # AWS OpenSearch cluster endpoint
region = "us-east-1"
service = 'es'

opensearch = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=("OPENSEARCH_USERNAME", "PASSWORD"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30, 
    retry_on_timeout=True,
    max_retries=3
)

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v)))
    return dict(items)

def process_file(key, documents, index_name):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    
    actions = []
    for doc in documents:
        # Parse the JSON string back into a dictionary
        content_dict = json.loads(doc.page_content)
        
        # Flatten the dictionary
        flattened_content = flatten_dict(content_dict)
        
        # Convert to a string representation
        content_str = json.dumps(flattened_content)        
        texts = text_splitter.split_text(content_str)
        
        for text in texts:
            embedding = embeddings.embed_query(text)
            action = {
                "_index": index_name,
                "_source": {
                    'filename': key,
                    'content': text,
                    'embedding': embedding
                }
            }
            actions.append(action)
    
    # Bulk index the documents
    if actions:
        helpers.bulk(opensearch, actions)

def create_index(client, index_name):
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 4
            }
        },
        'mappings': {
            'properties': {
                'filename': {'type': 'keyword'},
                'content': {'type': 'text'},
                'embedding': {'type': 'dense_vector', 'dims': 1536} 
            }
        }
    }
    
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=index_body)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

def process_all_json_files(directory_path, index_name):
    create_index(opensearch, index_name)
    
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    total_files = len(json_files)
    
    with tqdm(total=total_files, desc="Processing JSON files") as pbar:
        for doc in json_files:
            key = os.path.join(directory_path, doc)
            tqdm.write(f"Loading file: {key}")
            try:
                with open(key, 'r') as file:
                    json_data = json.load(file)
                
                # Convert the JSON data to a string
                json_string = json.dumps(json_data)
                
                # Create a Document object with the JSON string
                document = Document(page_content=json_string, metadata={"source": key})
                
                process_file(doc, [document], index_name)
                pbar.update(1)
                time.sleep(0.1)  # 100ms delay
            except Exception as e:
                tqdm.write(f"Error processing {key}: {str(e)}")
                continue

if __name__ == "__main__":
    # Change directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cve_folder = os.path.join(script_dir, "cve2")
    os.chdir(script_dir)
    process_all_json_files(cve_folder, "cve")