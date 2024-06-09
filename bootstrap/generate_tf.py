import os
from jinja2 import Environment, FileSystemLoader

BANNER = "\n\n#" + "=" * 10 + " AUTO GENERATED " + "=" * 10

providers_dicts = [
    {"alias": "general", "project": "general", "credentials": "general"}, 
    {"alias": "training", "project": "training", "credentials": "training"}, 
]

environment = Environment(loader=FileSystemLoader("templates/"))
provider_template = environment.get_template("provider.txt")
provider_vars_template = environment.get_template("provider_vars.txt")

os.chdir("../terraform")
def providers(): 
    f = open("providers.tf", "w") 
    f.write(f"{BANNER}\n\n")
    for provider in providers_dicts:
        content = provider_template.render(provider)
        f.write(f"{content}\n")

def provider_vars(): 
    f = open("values.tfvars", "w")
    f.write(f"{BANNER}\n\n")
    f.write("providers=[\n")
    for provider in providers_dicts: 
        content = provider_vars_template.render(provider)
        f.write(f"{content},\n")
    f.write("]\n")

# def backend():
#     #TODO