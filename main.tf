resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "tfstate" {
  name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
  provider = google.general //TODO automate?  
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
#   encryption {
#     default_kms_key_name = google_kms_crypto_key.terraform_state_bucket.id
#   }
#   depends_on = [
#     google_project_iam_member.default
#   ]
}

# #========== AUTO GENERATED ==========
# module "access" {
#     source = "./modules/access"
#     providers = {
#         google.general = google.general
# 		google.training = google.training
#     }
# }