import terraform 

def init_and_apply(): 
    tf = terraform.Terraform(working_dir="../terraform")
    tf.init() 
    tf.apply(skip_plan=True) #TODO: with the values.tfvars file? 