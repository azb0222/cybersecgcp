from gcloud import resource_manager
from google.cloud import iam_admin, storage, service_usage, billing
from googleapiclient import discovery

import random
import string
from os.path import join, isfile
from os import system, makedirs

from config import PROJECT_DATA_T, KEY_PATH, ActionState

print("[INFO] Creating GCP clients...")

resource_client = resource_manager.Client()
iam_client = iam_admin.IAMClient()
discovery_client = discovery.build('iam', 'v1')
service_client = service_usage.ServiceUsageClient()
billing_client = billing.CloudBillingClient()

def __make_project(project_id: str, project_name: str) -> ActionState:    
        project = resource_client.new_project(
            project_id,
            name=project_name,
        )

        if project_id in project_ids:
            print(f"[INFO] Project {project_id} already exists")
            return ActionState.EXISTS 
        
        print(f"[INFO] Creating project {project_id}")
        try:
            project.create()
            project.labels = {"source": "tf"}
            project.update()
            
            return ActionState.COMPLTE
        except Exception as e:
            print(f"[ERROR] Unable to create project {project_id} because:\n{e}") 
            return ActionState.FAILED

#TODO make seperate action states for each api
def __enable_apis(project_id : str, apis : list[str]) -> ActionState:
    print(f"[INFO] Enabling APIs for {project_id}...")
    try:
        for api in apis:
            print(f"[INFO] Enabling {api} API...")
            req = service_usage.EnableServiceRequest(name=f"projects/{project_id}/services/{api}.googleapis.com")
            resp = service_client.enable_service(request=req).result()
            if(resp.service.state != service_usage.State.ENABLED):
                raise Exception(f"Failed to enable {api}")
        return ActionState.COMPLTE
    except Exception as e:
        print(f"[ERROR] Unable to enable apis for {project_id} because:\n{e}") 
        return ActionState.FAILED

def __link_billing_account(project_id, billing_account_id):
    print(f"[INFO] Linking billing account {billing_account_id} to project {project_id}...")
    try:
        resource = f"projects/{project_id}"
        project_billing_info = {"billing_account_name": f"billingAccounts/{billing_account_id}"} 
        req = billing.UpdateProjectBillingInfoRequest(
            name=resource,
            project_billing_info=project_billing_info
            )
        billing_client.update_project_billing_info(request=req)
        return ActionState.COMPLTE
    except Exception as e:
        print(f"[ERROR] Unable to link billing account {billing_account_id} to {project_id} because:\n{e}") 
        return ActionState.FAILED

def __make_service_account(project_id, account_id, resource) -> ActionState:
    accounts = iam_client.list_service_accounts({"name": f"projects/{project_id}"})    
    accounts = map(lambda account : account.name, accounts)

    if resource in accounts:
        print(f"[INFO] Account {account_id} already exists")
        return ActionState.EXISTS
    
    print(f"[INFO] Creating account {account_id}")
    try:
        iam_client.create_service_account({
                "name": f"projects/{project_id}",
                "account_id": account_id
        })
        return ActionState.COMPLTE
    except Exception as e:
        print(f"[ERROR] Failed to create account {account_id} because:\n{e}")
        return ActionState.FAILED

def __config_service_account(project_id, principal) -> ActionState:
    # create service account IAM policymakedirs binding
    # TODO create custom role for service accounts
    print(f"[INFO] Creating role binding for {principal}")
    try:
        resource = f"projects/{project_id}/serviceAccounts/{principal}"
        policy = discovery_client.projects().serviceAccounts().getIamPolicy(resource=resource).execute()
        if not "bindings" in policy:
            policy["bindings"] = []
        policy["bindings"].append({
                "role": "roles/editor",
                "members": [
                    f"serviceAccount:{principal}"
                ]
            })

        body = {"policy": policy}
        discovery_client.projects().serviceAccounts().setIamPolicy(resource=resource, body=body).execute()
        return ActionState.COMPLTE
    except Exception as e:
        print(f"[ERROR] Failed to create role binding for {principal} because:\n{e}")
        return ActionState.FAILED

def __make_service_account_key(account_id, resource, project_data) -> ActionState:
    # create service account key
    key_file_name = f"{join(KEY_PATH, account_id)}.json"
    if isfile(key_file_name):
        print(f"[INFO] Key for {account_id} already exists")
        #TODO make not hardcoded
        project_data['credentials'] = f"../keys/{account_id}.json"
        return ActionState.EXISTS
    
    print(f"[INFO] Generating key for {account_id}")
    try:
        key = iam_client.create_service_account_key({
            "name": resource
        })
        with open(key_file_name, 'wb') as f:
            f.write(key.private_key_data)
        #TODO make not hardcoded
        project_data['credentials'] = f"../keys/{account_id}.json"
        return ActionState.COMPLTE
    except Exception as e:
        print(f"[ERROR] Failed to generate key for {account_id} because:\n{e}")
        return ActionState.FAILED

def __make_tfstate_bucket(project_id) -> tuple[ActionState, storage.Bucket | None]:  
    storage_client = storage.Client(project=project_id) #the general project
    random_string = ''.join(random.choices(string.ascii_lowercase+ string.digits, k=6))
    bucket_name = random_string + "_umasscybersec_tfstate"
    
    print(f"[INFO] Creating bucket {bucket_name} in the US")
    try:
        bucket = storage_client.bucket(bucket_name)
        new_bucket = storage_client.create_bucket(bucket, location="us")
        return ActionState.COMPLTE, new_bucket
    except Exception as e:
        print(f"[ERROR] Failed to generate bucket because:\n{e}")
        return ActionState.FAILED, None

def create_gcp(project_data : PROJECT_DATA_T) -> tuple[dict[str, dict[str, ActionState]], storage.Bucket | None]:
    global project_ids
    
    makedirs(KEY_PATH, exist_ok=True)
    all_action_states = {}

    billing_account_id = project_data["billing_account_id"]
    tf_bucket_project_name = project_data['tf_state_project']

    print("[INFO] Retrieving existing projects...")
    project_ids = list(map(lambda proj : proj.project_id, resource_client.list_projects()))
    print(f"[INFO] Found the following projects already: {project_ids}")

    for project_name in project_data['providers']:
        project_id = project_data["project_id_prefix"] + project_name 
        account_id = f"tf-sa1-{project_name}"
        principal = f"{account_id}@{project_id}.iam.gserviceaccount.com"
        resource = f"projects/{project_id}/serviceAccounts/{principal}"

        apis = project_data['providers'][project_name]['apis']

        all_action_states[project_name] = action_states = {}

        resp = __make_project(project_id, project_name)
        action_states['make_project'] = resp
        if resp == ActionState.FAILED:
            action_states["enable_apis"] = action_states["link_billing"] = action_states['make_account'] = action_states['config_account'] = action_states['make_key'] = ActionState.FAILED
            continue

        resp = __make_service_account(project_id, account_id, resource)
        action_states['make_account'] = resp
        if resp == ActionState.FAILED:
            action_states['config_account'] = action_states['make_key'] = ActionState.FAILED
            continue

        action_states['make_key'] = __make_service_account_key(account_id, resource, project_data['providers'][project_name])
        action_states['config_account'] = __config_service_account(project_id, principal)
        action_states['enable_apis'] = __enable_apis(project_id, apis)
        action_states['link_billing'] = __link_billing_account(project_id, billing_account_id)

    all_action_states[tf_bucket_project_name]['make_bucket'], bucket = __make_tfstate_bucket(project_data['project_id_prefix'] + tf_bucket_project_name)

    return all_action_states, bucket


if __name__ == "__main__":
    create_gcp()