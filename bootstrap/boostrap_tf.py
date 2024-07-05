# Done!!

import python_terraform 

from config import TERRAFORM_PATH

def init_and_apply():
    print("[INFO] Bootstraping terraform")
    tf = python_terraform.Terraform(working_dir=TERRAFORM_PATH)
    tf.init() 
    tf.apply(skip_plan=True)

if __name__ == "__main__":
    init_and_apply()