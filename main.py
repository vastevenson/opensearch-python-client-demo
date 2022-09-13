from opensearchpy import OpenSearch

host = 'search-vs-test-domain-l2czunaivht4bi7enm4zrfcg44.us-east-2.es.amazonaws.com'
port = 9200
auth = ('admin', 'Password1!') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = 'python-test-index'

def create_index(index_name):
    # Create an index with non-default settings.
    # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html#bp-sharding
    # shards should correspond to 10-30GB where search latency is objective
    # should be 30-50GB for write-heavy jobs like log analytics
    # by default, each index == 5 primary shards + 1 replica/primary == 10x total shards
    # replica shard == copy of a primary shard
    # shards are distributed amongst nodes for resilience
    # index > shards > multiple nodes (assuming you have more than 1)
    # lower shard count == faster reads
    # higher shard count == faster writes
    index_body = {
      'settings': {
        'index': {
          'number_of_shards': 1
        }
      }
    }

    response = client.indices.create(index_name, body=index_body)
    print('\nCreating index:')
    print(response)

# getting lots of timeouts - make sure the sec group for the cluster allows http and https traffic! 
create_index(index_name)
print()

def insert_doc_to_index(index_name):
    # Add a document to the index.
    document = {
      'title': 'Moneyball',
      'director': 'Bennett Miller',
      'year': '2011'
    }
    id = '1'

    response = client.index(
        index = index_name,
        body = document,
        id = id,
        refresh = True
    )

    print('\nAdding document:')
    print(response)

# Search for the document.
q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)
print('\nSearch results:')
print(response)

# Delete the document.
response = client.delete(
    index = index_name,
    id = id
)

print('\nDeleting document:')
print(response)

# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)