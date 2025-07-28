# Gets us our OpenWeatherMap API Key, which will either be loaded via .env
# (locally) or via Google Cloud Secrets Manager (deployed)

import os
from dotenv import load_dotenv
from google.cloud import secretmanager

# Google Cloud Service account was granted Secret Manager Secret Accessor
# IAM Role ("Allows accessing the payload of secrets")
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    
    return response.payload.data.decode("UTF-8")

# If we're operating in Google App Engine Standard, then retrieve the
# API key via the secrets manager (only Service account has permission).
# Otherwise, retrieve the API via local .env file (which doesn't work
# with Google App Engine)
def get_api_key(API_KEY):
    if os.getenv('GAE_ENV', '').startswith('standard'):
        return get_secret(API_KEY)
    else:
        load_dotenv()
        return os.getenv(API_KEY)