from gcloud import resource_manager
from typing import Optional
from google.cloud import iam_admin_v1, storage
from google.cloud.iam_admin_v1 import types
import random
import string

from config import PROJECT_ID_PREFIX, PROVIDERS

client = resource_manager.Client()

def projects(): 
    for provider in PROVIDERS:
        project_id = PROJECT_ID_PREFIX + provider['project'] 
        try:
            client.fetch_project(project_id)
            print("alr created")
            break
        except Exception as e: 
            print("project not created")
        project = client.project(
            project_id,
            name=provider["project"],
        )
        project.create()
        project.labels = {"SOURCE": "TF"}
        project.update()

#TODO: only create service accounts if they don't exist
def service_accounts():
    for provider in PROVIDERS:
        # create service account
        project_id = PROJECT_ID_PREFIX + provider['project'] 
        create_service_account(project_id, "tftestasritha")
        # create service account key 

        # create service account IAM policy binding 

def tfstate_bucket(): 
    storage_client = storage.Client(project=PROVIDERS[0]["project"]) #the general project
    random_string = ''.join(random.choices(string.ascii_lowercase+ string.digits, k=6))
    bucket_name = random_string + "_umasscybersec_tfstate"
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket



#TODO: fix i dont need a seperate helper function for this 
def create_service_account(
    project_id: str, account_id: str, display_name: Optional[str] = None
) -> types.ServiceAccount:
    """
    Creates a service account.

    project_id: ID or number of the Google Cloud project you want to use.
    account_id: ID which will be unique identifier of the service account
    display_name (optional): human-readable name, which will be assigned to the service account
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.CreateServiceAccountRequest()

    request.account_id = account_id
    request.name = f"projects/{project_id}"

    service_account = types.ServiceAccount()
    service_account.display_name = display_name
    request.service_account = service_account
    iam_admin_client.get_service_account()
    account = iam_admin_client.create_service_account(request=request)

    print(f"Created a service account: {account.email}")
    return account

