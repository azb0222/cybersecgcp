module "umassctf_internal_2024" {
  source = "./modules/umassctf_internal_2024"
  region = var.region
  project_id = var.project_id
  project_number = var.project_number
}