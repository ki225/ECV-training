import json
import os
from typing import Dict, Any, List
from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from tqdm.auto import tqdm  # Changed this line
import time
from langchain.text_splitter import CharacterTextSplitter


AZURE_OPENAI_EMBEDDING_KEY = "text-embedding-3-small"
os.environ["AZURE_OPENAI_API_KEY"] = "aa399c19184d4704a059e787e1dd7c79"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://intern-2024-h2.openai.azure.com/"

# Set up Azure OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDING_KEY,
    openai_api_version="2023-05-15",
)

# Set up OpenSearch client
host = "search-kiki-waf-m-skwshybharinuz57ouxxv6xddy.us-east-1.es.amazonaws.com"  # OpenSearch cluster endpoint
region = "us-east-1"
service = 'es'

opensearch = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=("kiki-waf-m", "1qaz2wsx#EDC"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30, 
    retry_on_timeout=True,
    max_retries=3
)

# Function to load HTML from S3, create embedding, and index in OpenSearch
def process_file(key, documents, index_name):
    # Split text (optional, depending on your needs)
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

def process_all_json_files(directory_path, index_name):
    # Step 1: Open the directory and count the PDF files
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    total_files = len(json_files)
    docs = json_files
    
    # Now process the files                
    with tqdm(total=total_files, desc="Processing JSON files") as pbar:
        for doc in docs:
            key = os.path.join(directory_path, doc)
            tqdm.write(f"Loading file: {key}")  # This will print without disrupting the progress bar
            loader = JSONLoader(key)
            document = loader.load()
            process_file(doc, document, index_name)
            pbar.update(1)
            time.sleep(0.1)  # 100ms delay



if __name__ == "__main__":
    # Change directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cve_folder = os.path.join(script_dir, "cve")
    os.chdir(script_dir)
    process_all_json_files(cve_folder, "cve")