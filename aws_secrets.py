import boto3
from botocore.exceptions import ClientError
import logging

def get_secret_string(secret_name):
    """
    Retrieve plain string value from AWS Secrets Manager.
    
    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        
    Returns:
        str or None: Secret value or None if retrieval fails
    """
    
    client = boto3.client('secretsmanager', region_name='us-west-2')  
    try:
        resp = client.get_secret_value(SecretId=secret_name)
        
        if 'SecretString' in resp:
            secret_string = eval(resp['SecretString'])
            for key in secret_string:
                return secret_string[key]
        else:
            logging.error(f"Secret {secret_name} does not contain SecretString")
            return None
    except ClientError as e:
        logging.error(f"Secrets Manager get_secret_value failed for {secret_name}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error reading secret {secret_name}: {e}")
    return None