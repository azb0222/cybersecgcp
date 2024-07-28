# Done!!

import python_terraform 

from config import TERRAFORM_PATH, ActionState

def init_and_apply() -> ActionState:
    print("[INFO] Bootstrapping terraform")
    try:
        tf = python_terraform.Terraform(working_dir=TERRAFORM_PATH)
        tf.init() 
        tf.apply(skip_plan=True)
        return ActionState.COMPLETE
    except Exception as e:
        print(f"[ERROR] Unable to bootstrap terraform because:\n{e}")
        return ActionState.FAILED

if __name__ == "__main__":
    init_and_apply()