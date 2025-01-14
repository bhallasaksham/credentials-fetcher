import boto3
import json
from parse_data_from_json import (number_of_gmsa_accounts, netbios_name,
                                  username, password, directory_name)

def create_secrets():
    # Initialize the AWS Secrets Manager client
    client = boto3.client('secretsmanager')

    # Base path for the secrets
    base_path = "aws/directoryservice/contoso/gmsa"

    for i in range(1, number_of_gmsa_accounts + 1):
            # Create the secret name
            secret_name = f"{base_path}/WebApp0{i}"

            # Create the secret value
            secret_value = {
                "username": username,
                "password": password,
                "domainName": directory_name,
                "distinguishedName": f"CN=WebApp0{i},OU=MYOU,OU=Users,OU={netbios_name},DC={netbios_name},DC=com"
            }

            try:
                # Create the secret
                response = client.create_secret(
                    Name=secret_name,
                    Description=f"Secret for WebApp0{i}",
                    SecretString=json.dumps(secret_value)
                )
                print(f"Created secret: {secret_name}")
            except client.exceptions.ResourceExistsException:
                print(f"Secret already exists: {secret_name}")
            except Exception as e:
                print(f"Error creating secret {secret_name}: {str(e)}")