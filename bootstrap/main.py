from os.path import join
import json

from config import DATA_PATH, ActionState
import generate_tf
import create_gcp 

#############################################################
# authenticate with 'gcloud auth application-default login' #
#############################################################

print("[INFO] Loading project data...")
try:
    with open(join(DATA_PATH, "project.json")) as f:
        project_data = json.load(f)
except Exception as e:
    print(f"[ERROR] Unable to load project data because:\n{e}")
    exit(1)

action_states = create_gcp.create_gcp(project_data)

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
        Enable APIs: {project_action_states['enable_apis'].value}
        Link billing account: {project_action_states['link_billing'].value}
""")

if any_state(ActionState.FAILED):
    print("[ERROR] GCP was not generated correctly so terraform will not be made. Please fix the errors and try again.")
    exit(1)
if any_state(ActionState.EXISTS):
    print("[WARNING] GCP had resources that already existed. These may not be configured correctly so please review them.")
    if input("Type yes to continue: ") != "yes":
        exit(1)

#TODO fix this(add logging and check if bucket made)
action_states = generate_tf.generate_tf(project_data)
print("""\n
Terraform Generation Summary:
""")
for task, result in action_states.items():
    print(f"    {task.replace("_", " ").capitalize()}: {result.value}")
print("\n")

if ActionState.FAILED in action_states.values():
    print("[ERROR] Unable to generate tf. Please fix the errors and try again.")
    exit(1)

print("Done!")