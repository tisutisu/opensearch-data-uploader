from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import os

# Create an index with non-default settings.
def create_index(client, index_name, number_of_shards=4):
    index_body = {
      'settings': {
        'index': {
          'number_of_shards': number_of_shards
        }
      }
    }
    response = client.indices.create(index_name, body=index_body)
    print('\nCreating index:')
    print(response)

def delete_index(client, index_name):
    response = client.indices.delete(
      index = index_name
    )
    print('\nDeleting index:')
    print(response)

def add_document_to_index(client, index_name, id, document):
    # Add a document to the index.
    response = client.index(
        index = index_name,
        body = document,
        id = id,
        refresh = True
    )
    print('\nAdding document:')
    print(response)

def delete_a_document(client, index_name, id):
    # Delete the document.
    response = client.delete(
        index = index_name,
        id = id
    )
    print('\nDeleting document:')
    print(response)

def search_document(client, index_name):
    # Sample search for the document.
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

def setup_os_client():
    host = os.environ['OS_HOST'] # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
    region = os.environ['OS_REGION']
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region)

    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return client

if __name__ == '__main__':
    index_name = 'test-index'
    client = setup_os_client()
    #create_index(client, index_name)
    #delete_index(client, index_name)

    # document = {
    #   'title': 'Moneyball',
    #   'director': 'Bennett Miller',
    #   'year': '2011'
    # }
    # id = '1'
    # add_document_to_index(client, index_name, id, document)
    # delete_a_document(client, index_name, id)


