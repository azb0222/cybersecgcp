provider "google" {
    region = "us-east1"
    zone = "us-east1-b"
}

provider "google" { 
    alias = "general"
    project = "umass-cybersec-general"
    credentials = "./keys/general.json"
    region = "us-east1"
    zone = "us-east1-b"
}

provider "google" { 
    alias = "training"
    project = "umass-cybersec-training"
    credentials = "./keys/training.json"
    region = "us-east1"
    zone = "us-east1-b"
}
