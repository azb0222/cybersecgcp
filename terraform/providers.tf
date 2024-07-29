#========== AUTO GENERATED ==========

provider "google" { 
    alias = "general"
    project = "general"
    credentials = "../keys/tf-sa1-general.json"
    region = "us-east1"
    zone = "us-east1-b"
}
provider "google" { 
    alias = "training"
    project = "training"
    credentials = "../keys/tf-sa1-training.json"
    region = "us-east1"
    zone = "us-east1-b"
}
