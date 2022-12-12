## opensearch-data-uploader
Tool to upload data from yaml file to opensearch instance in AWS

### Pre-requisites

- python 3.9
- pip install -r requirements.txt
- create the aws credentials file in the default location ~/.aws/credentials and specify the access key and secret access key as below.
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

### Usage

```
export OS_HOST='my-test-domain.us-east-1.es.amazonaws.com'
export OS_REGION='us-east-1'
export KPI_YAML_FILE='kpi.yaml'
python upload_data.py
```