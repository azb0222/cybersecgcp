resource "google_artifact_registry_repository" "ctfd-registry" { #TODO: pass in var here for each module to have {project-id}-ctfd-registry
  location      = "us-central1" #PASS in? 
  repository_id = "my-repository"
  description   = "example docker repository"
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "ctfd" {
  name     = "cloudrun-service"
  location = "us-central1"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }
}
