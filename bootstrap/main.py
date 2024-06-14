from os.path import join
import json

from config import DATA_PATH
import generate_tf
import create_gcp 
import boostrap_tf 

with open(join(DATA_PATH, "project.json")) as f:
    projects = json.load(f)

# authenticate with `gcloud auth application-default login`
create_gcp.projects(projects)
create_gcp.service_accounts(projects)
# bucket = create_gcp.tfstate_bucket()

# generate_tf.providers() 
# generate_tf.backend(bucket)

# boostrap_tf.init_and_apply()

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