from opensearchpy import OpenSearch, RequestsHttpConnection

opensearch = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

def create_index(index_name):
    index_body = {
        "settings": {
            "index": {
                "number_of_shards": 4,
                "number_of_replicas": 1
            },
            "analysis": {
                "analyzer": {
                    "json_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "char_filter": ["json_strip"],
                        "filter": ["lowercase", "stop", "snowball"]
                    }
                },
                "char_filter": {
                    "json_strip": {
                        "type": "pattern_replace",
                        "pattern": "[{}\\[\\]\"]",
                        "replacement": " "
                    }
                }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "json_analyzer"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 1536,
                    "method": {
                        "name": "hnsw",
                        "space_type": "l2",
                        "engine": "nmslib"
                    }
                },
                "filename": {"type": "keyword"},
                "last_modified": {"type": "date"}
            }
        }
    }

    if not opensearch.indices.exists(index_name):
        opensearch.indices.create(index_name, body=index_body)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")
        
index_name = 'cve'
create_index(index_name)