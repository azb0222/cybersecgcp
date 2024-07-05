resource "google_artifact_registry_repository" "challenge-images" {
  location      = var.region
  repository_id = "challenge-images"
  description   = "example docker repository"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "ctfd-images" {
  location      = "us-central1"
  repository_id = "my-repository"
  description   = "example docker repository"
  format        = "DOCKER"
}

