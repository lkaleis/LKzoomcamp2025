terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  project = "neon-runway-447221-q8"
  region  = "northamerica-northeast2"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "neon-runway-447221-q8-terra-bucket"
  location      = "northamerica-northeast2"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
