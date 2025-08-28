terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Create a Cloud Storage bucket for chunks with autoclass
resource "google_storage_bucket" "chunk_store" {
  name          = "${var.project_id}-chunk-store"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = var.force_destroy

  autoclass {
    enabled = true
  }

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

# Create Firestore Database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.firestore_region
  type        = "FIRESTORE_NATIVE"
  delete_protection_state = "DELETE_PROTECTION_DISABLED"
}

# Create Pub/Sub topic for chunk processing
resource "google_pubsub_topic" "chunk_processing" {
  name = "chunk-processing-topic"
}

# Create Pub/Sub subscription for storage worker
resource "google_pubsub_subscription" "storage_worker" {
  name  = "storage-worker-subscription"
  topic = google_pubsub_topic.chunk_processing.name

  ack_deadline_seconds = 300
  message_retention_duration = "604800s" # 7 days

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}

# Create Spanner Instance
resource "google_spanner_instance" "main" {
  name         = "drdr-spanner-instance"
  config       = "regional-${var.region}"
  display_name = "DRDR Main Instance"
  num_nodes    = var.spanner_nodes
  labels = {
    "environment" = var.environment
  }
}

# Create Spanner Database
resource "google_spanner_database" "chunk_index" {
  instance = google_spanner_instance.main.name
  name     = "chunk-index"
  ddl = [
    <<EOF
    CREATE TABLE Chunks (
        ChunkId STRING(64) NOT NULL,
        Created TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
        Size INT64 NOT NULL,
        ContainerObject STRING(256) NOT NULL,
        CompressionType STRING(16) NOT NULL DEFAULT 'NONE',
        EncryptionKey STRING(128)
    ) PRIMARY KEY (ChunkId);
    EOF
  ]

  deletion_protection = false
}

# Create Service Account for Cloud Run services
resource "google_service_account" "drdr_worker" {
  account_id   = "drdr-worker"
  display_name = "DRDR Cloud Run Service Account"
}

# IAM bindings for Service Account
resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.drdr_worker.email}"
}

resource "google_project_iam_member" "spanner_user" {
  project = var.project_id
  role    = "roles/spanner.databaseUser"
  member  = "serviceAccount:${google_service_account.drdr_worker.email}"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.drdr_worker.email}"
}

resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.drdr_worker.email}"
}

# Output important values
output "project_id" {
  value = var.project_id
}

output "chunk_bucket_name" {
  value = google_storage_bucket.chunk_store.name
}

output "upload_service_url" {
  value = google_cloud_run_service.upload_service.status[0].url
}
