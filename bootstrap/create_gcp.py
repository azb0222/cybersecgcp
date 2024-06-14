from gcloud import resource_manager
from google.cloud import iam_admin, iam_v2, storage
import random
import string
from os.path import join, isfile

from config import PROJECT_DATA_T, KEY_PATH

def projects(project_data : PROJECT_DATA_T) -> dict[str, bool]: 
    client = resource_manager.Client()

    for project_name in project_data['providers']:
        project_id = project_data['project_id_prefix'] +  project_name
        
        project = client.new_project(
            project_id,
            name=project_name,
        )
        
        if project.exists():
            print(f"[INFO] Project {project_id} already exists")
            project_data['providers'][project_name]['available'] = True
            continue

        try:
            print(f"[INFO] Creating project {project_id}")
            project.create()
            project.labels = {"SOURCE": "TF"}
            project.update()
            project_data['providers'][project_name]['available'] = True
        except Exception as e:
            print(f"[ERROR] Unable to create project {project_id} because:\n{e}") 
            project_data['providers'][project_name]['available'] = True
    

#TODO: only create service accounts if they don't exist
def service_accounts(project_data: PROJECT_DATA_T):
    client = iam_admin.IAMClient()
    policy_cient = iam_v2.PoliciesClient()
    
    for provider in project_data["providers"].values():
        project = provider["project"]
        project_id = project_data["project_id_prefix"] + project 
        service_account = f"tf-sa-{project}"
        resource = f"projects/{project_id}/serviceAccounts/{service_account}@{project_id}.iam.gserviceaccount.com"
        
        accounts = client.list_service_accounts({"name": project_id})    
        accounts = map(lambda account : account.name, accounts)
        
        if not resource in accounts:
            print(f"[INFO] Creating account {service_account}")
            client.create_service_account({
                "name": f"projects/{project_id}",
                "account_id": service_account
            })
        else:
            print(f"[INFO] Skipping account {service_account}. It already exists")
        

        # create service account IAM policy binding
        try:
            policy = client.get_iam_policy(resource=resource)
            # request = iam_policy_pb2.GetIamPolicyRequest(resource = resource)
            binding = {"role": "roles/editor"}
            policy["bindings"].append(binding)
            response = client.set_iam_policy(request=policy)
        except(Exception) as e:
            print(f"[INFO] Did not create account key for {project_id} because:")
            print(e)


        # create service account key
        if not isfile(join(KEY_PATH, project)):
            print(f"[INFO] Generating key for {service_account}")
            key = client.create_service_account_key({
                "name": resource  
            })
            with open(join(KEY_PATH, project), 'wb') as f:
                f.write(key.private_key_data)
        else:
            print(f"[INFO] Key for {service_account} already exists")
            

def tfstate_bucket(project_data: PROJECT_DATA_T) -> storage.Bucket: 
    storage_client = storage.Client(project=project_data["project_id_prefix"] + project_data["providers"]["general"]["project"]) #the general project
    random_string = ''.join(random.choices(string.ascii_lowercase+ string.digits, k=6))
    bucket_name = random_string + "_umasscybersec_tfstate"
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}")
    return new_bucket
