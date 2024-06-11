from os import chdir, path
from shutil import copy
from jinja2 import Environment, FileSystemLoader
from gcloud.storage import Bucket

from config import BANNER, TEMPLATE_PATH, TERRAFORM_PATH, DATA_PATH, PROJECT_DATA_T

environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

chdir(TERRAFORM_PATH)
def providers(project_data: PROJECT_DATA_T):
    provider_template = environment.get_template("provider.txt")
    with open("providers.tf", "w") as f:
        f.write(BANNER)
        for provider in project_data["providers"].values():
            content = provider_template.render(provider)
            f.write(f"{content}\n")

def data():
    copy(DATA_PATH, path.join(TERRAFORM_PATH, "data"))

def backend(bucket: Bucket):
    backend_template = environment.get_template("backend.txt")
    with open("backend.tf", "w") as f:
       f.write(BANNER)
       f.write(f"{backend_template.render(bucket_id=bucket.id)}")