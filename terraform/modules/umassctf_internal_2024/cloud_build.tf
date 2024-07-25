//https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github

/*
Due to receiving a 500 server error when attempting to create a personal access token while setting up the Github host connection programmatically, I followed the manual approach.
To maintain terraform as the source of truth, I ran the following import commands:
   - `terraform import module.umassctf_internal_2024.google_secret_manager_secret.github_token_secret projects/58401675291/secrets/umass-cybersec-connection-github-oauthtoken-aef47e`
   - `terraform import module.umassctf_internal_2024.google_secret_manager_secret_version.github_token_secret_version projects/58401675291/secrets/umass-cybersec-connection-github-oauthtoken-aef47e/versions/1`
   - `terraform import module.umassctf_internal_2024.google_cloudbuildv2_connection.umass_cybersec_connection projects/58401675291/locations/us-central1/connections/umass-cybersec-connection`

*/

//store authorization token for umass-cybersec Github account
resource "google_secret_manager_secret" "github_token_secret" {
    project = var.project_number
    secret_id = "umass-cybersec-connection-github-oauthtoken-aef47e"

    replication {
        user_managed {
            replicas {
                location = var.region
            }
        }
    }
}

resource "google_secret_manager_secret_version" "github_token_secret_version" {
    secret = google_secret_manager_secret.github_token_secret.id
    secret_data = "ghu_Re1WbPElYWvNvnIUo69RXh21skQiET0hUwEt" //TODO: move to terraform secret or file in .gitignore or something
}

//allow Cloud Build Service Agent account to access github_token_secret
data "google_iam_policy" "cloudbuild_service_agent_secretAccessor" {
    binding {
        role = "roles/secretmanager.secretAccessor"
        members = ["serviceAccount:service-${var.project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"]
    }
}

resource "google_secret_manager_secret_iam_policy" "cloudbuild_service_agent_secretAccessor_policy" {
    project = google_secret_manager_secret.github_token_secret.project
    secret_id = google_secret_manager_secret.github_token_secret.secret_id
    policy_data = data.google_iam_policy.cloudbuild_service_agent_secretAccessor.policy_data
}

//Github host connection
resource "google_cloudbuildv2_connection" "umass_cybersec_connection" {
    project = var.project_number
    location = var.region
    name = "umass-cybersec-connection"

    github_config {
        app_installation_id = 53067010
        authorizer_credential {
            oauth_token_secret_version = "projects/${var.project_id}/secrets/${google_secret_manager_secret.github_token_secret.secret_id}/versions/latest"
        }
    }

    depends_on = [google_secret_manager_secret_iam_policy.cloudbuild_service_agent_secretAccessor_policy]
}

//Github repo: UMassInternalCTF2024
resource "google_cloudbuildv2_repository" "UMassInternalCTF2024" {
    project = var.project_id
    location = var.region
    name = "UMassCTFInternal2024"
    parent_connection = google_cloudbuildv2_connection.umass_cybersec_connection.name
    remote_uri = "https://github.com/UMassCybersecurity/UMassInternalCTF2024.git"
}