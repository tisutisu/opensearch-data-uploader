from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import os
import yaml
import string
import random
from datetime import datetime

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

def read_metric_data(metric_file_name):
    with open(metric_file_name) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        kpi_data = content['kpi']
    for data in kpi_data:
        if data['name'] == 'usage':
            for metric in data['metrics']:
                if metric['name'] == 'Memory_MiB':
                    memory_average = metric['average']
                    memory_maximum = metric['maximum']
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {'date': dt_string, 'average' : float(memory_average), 'maximum': float(memory_maximum), 'average_threshold': 80, 'maximum_threshold': 110, 'value_unit': 'MiB'}    

def generate_id():
    n = 6
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

if __name__ == '__main__':
    index_name = 'test-index'
    client = setup_os_client()
    #create_index(client, index_name)
    #delete_index(client, index_name)
    # delete_a_document(client, index_name, id)

    metric_file_name = os.environ['KPI_YAML_FILE']
    doc = read_metric_data(metric_file_name)
    id = generate_id()
    print(f"Random Generated ID: {id}")
    add_document_to_index(client, index_name, id, doc)


    


