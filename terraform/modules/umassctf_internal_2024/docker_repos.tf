resource "google_artifact_registry_repository" "challenge-images" {
  location      = var.region
  repository_id = "challenges"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "ctfd-images" {
  location      = var.region
  repository_id = "ctfd"
  format        = "DOCKER"
}


#  umass-cybersec: github account used to authorize Github CloudBuild app actions; robot account
#tag images based on category

/*
cloud build -> builds docker image -> push to AR -> create CloudRun container
*/


