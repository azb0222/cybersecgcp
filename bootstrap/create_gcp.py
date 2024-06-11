from gcloud import resource_manager
from typing import Optional
from google.cloud import iam_admin, storage
import random
import string
from os.path import join
from google.iam.v1 import iam_policy_pb2  # type: ignore

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
        service_account = f"terraform_sa{project_id}"
        resource = f"projects/{project_id}/serviceAccounts/{service_account}"
        #resource = "projects/umass-cybersec-general/serviceAccounts/terraform-account@umass-cybersec-general.iam.gserviceaccount.com"
        try:
            client.create_service_account({
                "name": project_id,
                "account_id": service_account
            })
        except(Exception) as e:
            print(f"[INFO] Did not create account for {project_id} because:")
            print(e)
        # create service account key 
        try:
            key = client.create_service_account_key({
              "name": resource  
            })
            with open(join(KEY_PATH, provider["project"]), 'wb') as f:
                f.write(key.private_key_data)
        
        except(Exception) as e:
            print(f"[INFO] Did not create account key for {project_id} because:")
            print(e)
        
        # create service account IAM policy binding
        try:
            
            policy = client.get_iam_policy(resource=resource)
            # request = iam_policy_pb2.GetIamPolicyRequest(resource = resource)
            binding = {"role": "roles/editor"}
            policy["bindings"].append(binding)
            response = client.set_iam_policy(request=policy)
            
            
            

def tfstate_bucket(project_data: PROJECT_DATA_T) -> storage.Bucket: 
    storage_client = storage.Client(project=project_data["project_id_prefix"] + project_data["providers"]["general"]["project"]) #the general project
    random_string = ''.join(random.choices(string.ascii_lowercase+ string.digits, k=6))
    bucket_name = random_string + "_umasscybersec_tfstate"
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}")
    return new_bucket
