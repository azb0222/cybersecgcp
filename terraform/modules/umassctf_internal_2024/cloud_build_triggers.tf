//cloudbuild service account + necessary IAM permissions
//TODO: should this be in the other file?
resource "google_service_account" "cloudbuild_sa" {
  account_id = "cloudbuild-sa"
}

resource "google_project_iam_member" "cloudbuild_sa_act_as" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

resource "google_project_iam_member" "cloudbuild_sa_logs_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

resource "google_project_iam_member" "cloudbuild_sa_push_to_ar" {
  project = var.project_id
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

resource "google_project_iam_member" "cloudbuild_cloudrun_developer" {
  project = var.project_id
  role = "roles/run.developer"
  member = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

//create a cloudbuild trigger for each challenge
resource "google_cloudbuild_trigger" "chall_cloudbuild_trigger" {
  for_each = var.dynamic_challenges

  name = each.value.name
  location = var.region


  repository_event_config {
    repository = google_cloudbuildv2_repository.UMassInternalCTF2024.id
    push {
      branch = "dev"
    }
  }

  service_account = google_service_account.cloudbuild_sa.id

  build {
    timeout = "2400s" //40 minutes
    step {
      name = "gcr.io/cloud-builders/docker"
      dir = each.value.dir #TODO: there is deff a better way to do this. should not rebuild all the containers upon pushing to one, only based on subdirectory
      args = [
        "build", "-t",
        #currently each image is tagged with its category
        #TODO: what happens when you push again ie. v2
        "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.challenge-images.name}/${each.value.name}:${each.value.category}",
        "."
      ]
    }
    step {
      name = "gcr.io/cloud-builders/docker"
      dir = each.value.dir
      args = ["push", "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.challenge-images.name}/${each.value.name}:${each.value.category}"]
      timeout = "1200s" #TODO: idk if i need these timeouts
    }

    //creates a cloudrun container named after the challenge name
    //TODO: does this work, or does the cloudrun container alr have to exist, what if you need db or cache?
    step {
      name = "gcr.io/cloud-builders/gcloud"
      dir = each.value.dir
      args = ["run", "deploy", each.value.name, "--image", "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.challenge-images.name}/${each.value.name}:${each.value.category}", "--region", var.region, "--platform", "managed", "--allow-unauthenticated"]
    }
    options {
      logging = "CLOUD_LOGGING_ONLY"
    }
  }
}