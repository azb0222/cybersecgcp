from gcloud import resource_manager
from typing import Optional
from google.cloud import iam_admin, storage
import random
import string
import json
from os.path import join

from config import PROJECT_DATA_T, KEY_PATH

def projects(project_data : PROJECT_DATA_T): 
    client = resource_manager.Client()
    for provider in project_data["providers"].values():
        project_id = project_data["project_id_prefix"] + provider['project'] 
        
        print(f"[INFO] Creating project {project_id}")
        project = client.new_project(
            project_id,
            name=provider["project"],
        )
        if project.exists():
            print(f"[INFO] Project {project_id} already exists")
            continue
        project.create()
        project.labels = {"SOURCE": "TF"}
        project.update()            

#TODO: only create service accounts if they don't exist
def service_accounts(project_data: PROJECT_DATA_T):
    client = iam_admin.IAMClient()
        
    for provider in project_data["providers"].values():
        project_id = project_data["project_id_prefix"] + provider['project'] 

        try:
            client.create_service_account({
                "name": project_id,
                "account_id": "terraform_sa" + project_id
            })
        except(Exception) as e:
            print(f"[INFO] Did not create account for {project_id} because:")
            print(e)
        # create service account key 
        try:
            key = client.create_service_account_key({
              "name": project_id  
            })
            with open(join(KEY_PATH, provider["project"])) as f:
                json.dump(key, f)
        except(Exception) as e:
            print(f"[INFO] Did not create account key for {project_id} because:")
            print(e)


        
        # create service account IAM policy binding
        try:
            client.create_role
            p = client.get_iam_policy()
            p.       

def tfstate_bucket(project_data: PROJECT_DATA_T) -> storage.Bucket: 
    storage_client = storage.Client(project=project_data["project_id_prefix"] + project_data["providers"]["general"]["project"]) #the general project
    random_string = ''.join(random.choices(string.ascii_lowercase+ string.digits, k=6))
    bucket_name = random_string + "_umasscybersec_tfstate"
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}")
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
    account = iam_admin_client.create_service_account(request=request)

    print(f"Created a service account: {account.email}")
    return account

