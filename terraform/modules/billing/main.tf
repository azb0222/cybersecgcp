# data "google_billing_account" "billing_account" {
#   billing_account = "billingAccounts/01EE1A-159BAC-021ABD"
#   open         = true
# }

# // Billing Account IAM Policies 
# resource "google_billing_account_iam_binding" "devops_club" {
#   billing_account_id = data.google_billing_account.billing_account.id
#   role               = "roles/billing.admin"

#   //TODO: create a global object for DevOps Club members
#   members = [
#     "asrithabodepudi@gmail.com",
#   ]
# }

# resource "google_billing_account_iam_binding" "eboard" {
#   billing_account_id = data.google_billing_account.billing_account.id
#   role               = "roles/billing.viewer"
#   members = [
#     "larryliu@gmail.com",
#   ]
# }

# // Billing Account Budgets #TODO
# resource "google_billing_budget" "budget" {
#   billing_account = data.google_billing_account.billing_account.id
#   display_name = "Billing Alerts for Project"

#   budget_filter {
#     projects = ["projects/${data.google_project.project.number}"]
#   }

#   amount {
#     specified_amount {
#       currency_code = "USD"
#       units = "100"
#     }
#   }
#   threshold_rules {
#       threshold_percent =  0.5
#   }
# }