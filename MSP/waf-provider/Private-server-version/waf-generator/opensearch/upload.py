import json
import os
from typing import Dict, Any, List
from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
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

# Set up OpenSearch client
host = ""  # OpenSearch cluster endpoint
region = "us-east-1"
service = 'es'

opensearch = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=("", ""),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30, 
    retry_on_timeout=True,
    max_retries=3
)

# Function to load HTML from S3, create embedding, and index in OpenSearch
def process_file(key, documents, index_name):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings
    for doc in docs:
        embedding = embeddings.embed_query(doc.page_content)
        
        # Index in OpenSearch
        body = {
            'filename': key,
            'content': doc.page_content,
            'embedding': embedding
        }
        opensearch.index(index=index_name, body=body)

def dict_to_string(data):
    return json.dumps(data, indent=2)

def process_all_json_files(directory_path, index_name):
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    total_files = len(json_files)
    print(f"Total files found: {total_files}")

    with tqdm(total=total_files, desc="Processing JSON files") as pbar:
        for doc in json_files:
            key = os.path.join(directory_path, doc)
            tqdm.write(f"Loading file: {key}")
            try:
                loader = JSONLoader(key, jq_schema=".", text_content=False)
                documents = loader.load()
                
                # Convert each document's page_content (which is a dict) to a string
                for document in documents:
                    if isinstance(document.page_content, dict):
                        document.page_content = dict_to_string(document.page_content)
                
                process_file(doc, documents, index_name)
            except Exception as e:
                tqdm.write(f"Error processing {key}: {str(e)}")
            finally:
                pbar.update(1)



if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cve_folder = os.path.join(script_dir, "cve2")
    os.chdir(script_dir)
    process_all_json_files(cve_folder, "cve")