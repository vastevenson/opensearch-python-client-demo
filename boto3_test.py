import boto3

client = boto3.client('opensearch')
response = client.describe_domains(
    DomainNames=[
        'vs-test-domain',
    ]
)
print()
