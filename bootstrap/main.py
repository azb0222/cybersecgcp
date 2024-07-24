from os.path import join
import json

from config import DATA_PATH, ActionState
import generate_tf
import create_gcp 
import boostrap_tf 

#############################################################
# authenticate with `gcloud auth application-default login' #
#############################################################

print("[INFO] Loading project data...")
try:
    with open(join(DATA_PATH, "project.json")) as f:
        project_data = json.load(f)
except Exception as e:
    print(f"[ERROR] Unable to load project data because:\n{e}")
    exit(1)

action_states, bucket = create_gcp.create_gcp(project_data)

with open(join(DATA_PATH, "project-generated.json"), 'w') as f:
    json.dump(project_data, f)

def any_state(state: ActionState) -> bool:
    for p_action_states in action_states.values():
        for action_state in p_action_states.values():
            if action_state == state:
                return True
    return False

print("""\n
GCP Post Deployment Summary:
""")
for project in action_states:
    project_action_states = action_states[project]
    print(f"""{project}:
    Make project: {project_action_states['make_project'].value}
        Make service account: {project_action_states['make_account'].value}
            Make service account key: {project_action_states['make_key'].value}
            Configure service account: {project_action_states['config_account'].value}
""")
print(f"State Bucket: {action_states[project_data['tf_state_project']]["make_bucket"].value}\n\n")

if any_state(ActionState.FAILED):
    print("[ERROR] GCP was not generated correctly so terraform will not be made. Please fix the errors and try again.")
    exit(1)
if any_state(ActionState.EXISTS):
    print("[WARNING] GCP had resources that already existed. These may not be configured correctly so please review them.")
    if input("Type yes to continue: ") != "yes":
        exit(1)

#TODO fix this(add logging and check if bucket made)
action_states = generate_tf.generate_tf(project_data, bucket)
print("""\n\n
Terraform Generation Summary:
""")
for task, result in action_states.items():
    print(f"\t{task.replace("_", " ").capitalize()}: {result.value}")
print("\n\n")

if ActionState.FAILED in action_states.values():
    print("[ERROR] Unable to generate tf. Please fix the errors and try again.")
    exit(1)

if input("Ready to bootstap terraform! Type yes to continue: ") != "yes":
        exit(1)

boostrap_tf.init_and_apply()


'''
PROJECT_FILE = "data/projects.json"
KEY_PATH = "./keys"



def load_projects():
    global projects

    with open(PROJECT_FILE) as f:
        projects = json.load(f)

    if not "project_id" in projects:
        print("[ERROR] project_id not found")
        exit(1)

    if not "project_names" in projects:
        print("[ERROR] project_names not found")
        exit(1)

def setup_key_dir():
    os.system(f"sudo rm -rf {KEY_PATH}")
    os.makedirs(KEY_PATH)


def make_resources():
    setup_key_dir()
    for name in projects['project_names']:
        project_id = projects['project_id'] + name
        os.system(f"gcloud projects create {project_id} --name={name} --labels=SOURCE=TF")
        os.system(f"gcloud config set project {project_id}")
        os.system("gcloud iam service-accounts create terraform-account")
        os.system(f"gcloud projects add-iam-policy-binding {project_id} --member=serviceAccount:terraform-account@{project_id}.iam.gserviceaccount.com --role=roles/editor")
        os.system(f"gcloud iam service-accounts keys create ./keys/{name}.json --iam-account=terraform-account@{project_id}.iam.gserviceaccount.com")

def make_tf_files():
    # Providers
    # TODO: add BANNER in providers.tf too 
    with open("providers.tf", 'w') as f:
        f.write("""provider "google" {
    region = "us-east1"
    zone = "us-east1-b" 
}
""") #TODO: idk if we need to add the region + zone every time, or we can just have default for hte main provider "google"
        f.write("".join([f"""
provider "google" \u007b 
    alias = "{name}"
    project = "{projects['project_id']}{name}"
    credentials = "./keys/{name}.json"
    region = "us-east1"
    zone = "us-east1-b"
\u007d
""" for name in projects['project_names']]))

    # Provider Modules (in main.tf)
    provider_modules = "\n\t\t".join([ f"google.{name} = google.{name}" for name in projects['project_names']])

    with open("main.tf") as f:
        main_tf = f.read()

    banner_idx = main_tf.find(BANNER)
    if banner_idx != -1:
        main_tf = main_tf[:banner_idx]

    main_tf += f"""{BANNER}
module "access" \u007b
    source = "./modules/access"
    providers = \u007b
        {provider_modules}
    \u007d
\u007d"""

    with open("main.tf", "w") as f:
        f.write(main_tf)

load_projects()
make_resources()
make_tf_files()



'''
'''
script should: 
- create projects with gcloud cli 
- generate terraform.tfvars file with a list of the projects 
- tfstate bucket  
- call terraform init/apply 
- provision service accounts with tf as well 

setup includes: 
1) creating projects 
2) creating sevice accounts with appropriate permissions for each project 
3) setting up provider variables 
4) setting up general tf state bucket in general project
5) call terraform init/apply
'''