from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3

host = 'search-vs-test-domain-l2czunaivht4bi7enm4zrfcg44.us-east-2.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-2' # e.g. us-west-1

credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

index_name = 'python-test-index-2'

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

create_index(index_name)
print()