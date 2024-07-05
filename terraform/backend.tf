//https://cloud.google.com/docs/terraform/resource-management/store-state, this is how i created the bucket in Cloud Shell  
terraform {
 backend "gcs" {
   bucket  = "6186e1677ac0ea2d-bucket-tfstate" #TODO: use templating for this from the python script, or .tfvars?  
   prefix  = "terraform/state"
 }
}
