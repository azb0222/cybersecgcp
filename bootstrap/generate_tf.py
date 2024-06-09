import os
from config import BANNER, PROVIDERS, TEMPLATE_PATH, TERRAFORM_PATH
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
provider_template = environment.get_template("provider.txt")
provider_vars_template = environment.get_template("provider_vars.txt")

os.chdir(TERRAFORM_PATH)
def providers(): 
    f = open("providers.tf", "w") 
    f.write(f"{BANNER}\n\n")
    for provider in PROVIDERS:
        content = provider_template.render(provider)
        f.write(f"{content}\n")

def provider_vars(): 
    f = open("values.tfvars", "w")
    f.write(f"{BANNER}\n\n")
    f.write("providers=[\n")
    for provider in PROVIDERS: 
        content = provider_vars_template.render(provider)
        f.write(f"{content},\n")
    f.write("]\n")

# def backend():
#     #TODO