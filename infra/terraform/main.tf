terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.39.0"
    }
  }


  backend "gcs" {
    bucket = "boy-tf-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  credentials = file(var.credentials)

  project = var.project
  region  = var.region
  zone    = "${var.region}-c"
}

# TODO change name when front uses DNS entries
resource "google_cloud_run_service" "python_api" {
  name     = "boy-api-v2${var.run_version}"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project}/api:latest"
        env {
          name  = "APP_SANDBOX"
          value = true
        }
        env {
          name = "ANDROID_SERVICE_ACCOUNT"
          value_from {
            secret_key_ref {
              name     = "ANDROID-service-account"
              key = "latest"
            }
          }
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.python_api.location
  project     = google_cloud_run_service.python_api.project
  service     = google_cloud_run_service.python_api.name
  policy_data = data.google_iam_policy.noauth.policy_data
}