import python_terraform 

from config import TERRAFORM_PATH

def init_and_apply(): 
    tf = python_terraform.Terraform(working_dir=TERRAFORM_PATH)
    tf.init() 
    tf.apply(skip_plan=True) #TODO: with the values.tfvars file? 

if __name__ == "__main__":
    init_and_apply()