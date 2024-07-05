terraform {
 backend "gcs" {
   bucket  = "6186e1677ac0ea2d-bucket-tfstate" 
   prefix  = "terraform/state"
 }
}
