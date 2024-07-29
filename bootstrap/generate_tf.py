from shutil import copytree
from jinja2 import Environment, FileSystemLoader
from gcloud.storage import Bucket

from config import BANNER, TEMPLATE_PATH, from_terraform, DATA_PATH, PROJECT_DATA_T, ActionState

environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

def __make_providers(project_data: PROJECT_DATA_T) -> ActionState:
    print("[INFO] Generating provider.tf")
    try:
        provider_template = environment.get_template("provider.txt")
        with open(from_terraform("providers.tf"), "w") as f:
            f.write(BANNER)
            for project, provider in project_data["providers"].items():
                provider['project'] = project
                content = provider_template.render(provider)
                f.write(f"{content}\n")
        return ActionState.COMPLETE
    except Exception as e:
        print(f"[ERROR] Could not generate provider.tf because:\n{e}")
        return ActionState.FAILED

def __copy_data() -> ActionState:
    print("[INFO] Copying data into terraform")
    try:
        copytree(DATA_PATH, from_terraform("data"), dirs_exist_ok=True)
        return ActionState.COMPLETE
    except Exception as e:
        print(f"[ERROR] Could not copy data because:\n{e}")
        return ActionState.FAILED

# def __make_backend(bucket: Bucket) -> ActionState:
#     print("[INFO] Generating backend.tf")
#     try:
#         backend_template = environment.get_template("backend.txt")
#         with open(from_terraform("backend.tf"), "w") as f:
#             f.write(BANNER)
#             f.write(f"{backend_template.render(bucket_id=bucket.id)}")
#         return ActionState.COMPLETE
#     except Exception as e:
#         print(f"[ERROR] Could not generate backend.tf because:\n{e}")
#         return ActionState.FAILED
    
def generate_tf(project_data: PROJECT_DATA_T) -> dict[str, ActionState]:
    return {
        "make_providers": __make_providers(project_data),
        "copy_data": __copy_data(),
    }