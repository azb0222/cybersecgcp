//https://cloud.google.com/docs/terraform/resource-management/store-state, this is how i created the bucket in Cloud Shell  


terraform {
 backend "gcs" {
   bucket  = "6186e1677ac0ea2d-bucket-tfstate"
   prefix  = "terraform/state"
 }
}
