import json
import os

with open("data/projects.json") as f:
    projects = json.load(f)

if not "project_id" in projects:
    print("[ERROR] project_id not found")

if not "project_names" in projects:
    print("[ERROR] project_names not found")

tf_file = ""

for name in projects['project_names']:
    full_name = projects['project_id'] + name
    os.system(f"gcloud projects create {full_name} --name={name}")

    tf_file += f"""
import \u007b 
    id = "{full_name}"
    to = google_project.{name}
\u007d
    """

with open("projects.tf", "w") as f:
    f.write(tf_file)