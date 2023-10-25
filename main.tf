terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}


locals {
  project = "air-paradise" # Google Cloud Platform Project ID
  region  = "us-west1"
}

variable "SPOTIPY_CLIENT_ID" {
  type = string
}
variable "SPOTIPY_CLIENT_SECRET" {
  type = string
}

resource "random_id" "default" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name                        = "${random_id.default.hex}-gcf-source" # Every bucket name must be globally unique
  location                    = "US"
  uniform_bucket_level_access = true
  project                     = local.project
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "/tmp/function-source.zip"
  source_dir  = "src/"
}

resource "google_storage_bucket_object" "object" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path # Add path to the zipped function source code
}

resource "google_cloudfunctions2_function" "function" {
  name        = "scrobbler"
  description = "Scrobble RP"
  location    = local.region
  project     = local.project
  build_config {
    runtime     = "python310"
    entry_point = "mainHTTP" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
    environment_variables = {
      SPOTIPY_CLIENT_ID     = var.SPOTIPY_CLIENT_ID
      SPOTIPY_CLIENT_SECRET = var.SPOTIPY_CLIENT_SECRET
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}

output "function_uri" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}

resource "google_service_account" "service_account" {
  account_id   = "invoker"
  display_name = "Scrobbler Cloud Function Invoker Service Account"
  project      = local.project
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  cloud_function = google_cloudfunctions2_function.function.name
  role           = "roles/viewer"
  member         = google_service_account.service_account.member
  project        = local.project
  depends_on     = [google_cloudfunctions2_function.function]
}

# https://github.com/hashicorp/terraform-provider-google/issues/15264

data "google_iam_policy" "invoker" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_v2_service_iam_policy" "invoker" {
  location    = google_cloudfunctions2_function.function.location
  name        = google_cloudfunctions2_function.function.name
  project     = local.project
  policy_data = data.google_iam_policy.invoker.policy_data
}

resource "google_cloud_scheduler_job" "job" {
  name             = "scrobbler-cloudfunction-scheduler"
  description      = "Trigger the ${google_cloudfunctions2_function.function.name} Cloud Function every 30 mins."
  schedule         = "59,29 * * * *" # Every 30 mins
  time_zone        = "Australia/Sydney"
  attempt_deadline = "320s"
  region           = local.region
  project          = local.project

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.function.service_config[0].uri

    oidc_token {
      service_account_email = google_service_account.service_account.email
    }
  }
}
