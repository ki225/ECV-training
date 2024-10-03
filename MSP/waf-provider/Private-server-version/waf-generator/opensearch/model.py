import boto3
import base64
import httpx
import os
import json
import uuid
import re
import requests
from opensearchpy import OpenSearch # low level client

# import feedback_logger
# from environ import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, SERPER_API_KEY, AOS_HOST, AOS_PWD, AOS_UNAME, AZURE_OPENAI_EMBED_KEY, AZURE_OPENAI_DEPLOYMENT
# from prompts import SUMMARIZE_PROMPT, INQUIRY_PROMPT_WITH_TOOLS, ANSWERING_PROMPT, IMAGE_PROMPT
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_aws import ChatBedrock
from openai import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import OpenSearchVectorSearch
# Callbacks
from langchain_community.callbacks.manager import get_bedrock_anthropic_callback
from langchain_community.callbacks.manager import get_openai_callback

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
session = boto3.Session()


os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
# os.environ["SERPER_API_KEY"] = SERPER_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
os.environ["AZURE_OPENAI_DEPLOYMENT"] = AZURE_OPENAI_DEPLOYMENT

session_id = "SBR-#INC91"
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
parser = StrOutputParser()

# Set up Anthropic Bedrock
model = ChatBedrock(
    model_id="model-id",
    model_kwargs=dict(temperature=0),
    # other params...
)

os_client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    # connection_class=RequestsHttpConnection
)



# Set up Azure OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDING_KEY,
    openai_api_version="2023-05-15",
)


docsearch = OpenSearchVectorSearch(
    index_name="cve",  # index name
    embedding_function=embeddings,
    opensearch_url=os_url,
    http_auth = auth
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10,
        "vector_field":"embedding",
        "text_field":"content", 
    }
)

# document_retiever = create_retriever_tool(
#     retriever,
#     "AWS FAQ",
#     "Searches and retrieves information from AWS documentation and FAQs. Use this tool when you need specific details about AWS services, features, or best practices.",
# )

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2023-05-15",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)



def ask_question(question, chat_history):
    # Use invoke instead of get_relevant_documents
    docs = retriever.invoke(question)

    if not docs:
        return "I couldn't find any relevant information to answer your question."
    
    # If docs is a list of Document objects, extract page_content
    if isinstance(docs[0], Document):
        context = "\n\n".join([doc.page_content for doc in docs])
    else:
        # If docs is already a list of strings, join them directly
        context = "\n\n".join(docs)

    prompt = f"""Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    If user give you CVE ID, you can check 'cveMetadata_cveId' and ouput the information under that CVE ID.

    Context:
    {context}

    Question: {question}

    Answer:"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about AWS based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=150
    )
    return response.choices[0].message.content

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model=os.getenv("AZURE_OPENAI_EMBED_MODEL")  # Replace with your embedding model name
    )
    return response.data[0].embedding


def search_opensearch(query, index_name="cve", k=100):
    # Get the embedding for the query
    query_embedding = get_embedding(query)
    

    # Prepare the OpenSearch query
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding}
            }
        }
    }

    # Execute the search
    response = os_client.search(
        index=index_name,
        body={
            "size": k,
            "query": script_query,
            "_source": ["content"]  # Only retrieve the 'content' field
        }
    )

    # Extract and return the content from the hits
    results = [hit["_source"]["content"] for hit in response["hits"]["hits"]]
    return results

def print_opensearch_sample(index_name="cve", sample_size=100):
    """
    Print a sample of documents from the specified OpenSearch index.
    
    :param index_name: Name of the index to sample from
    :param sample_size: Number of documents to retrieve and print
    """
    try:
        # Query to get a random sample of documents
        query = {
            "size": sample_size,
            "query": {
                "function_score": {
                    "query": {"match_all": {}},
                    "random_score": {}
                }
            }
        }
        
        response = os_client.search(index=index_name, body=query)
        
        print(f"Sample of {sample_size} documents from index '{index_name}':")
        for hit in response['hits']['hits']:
            print(f"\nDocument ID: {hit['_id']}")
            print("Content:")
            # Assuming 'content' field exists, adjust if your field name is different
            print(hit['_source'].get('content', 'No content field found')[:200] + '...')  # Print first 200 characters
        
    except Exception as e:
        print(f"Error retrieving sample from OpenSearch: {str(e)}")

def call(chat_history):
    # Example usage
    question = "give me informatoin for CVE-2023-0258"
    answer = ask_question(question, chat_history)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print_opensearch_sample()
    results = search_opensearch("CVE-2023-0258")
    print(results)
    return answer