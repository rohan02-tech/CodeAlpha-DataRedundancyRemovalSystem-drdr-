variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "firestore_region" {
  description = "The region for Firestore"
  type        = string
  default     = "nam5"
}

variable "spanner_nodes" {
  description = "Number of Spanner nodes"
  type        = number
  default     = 1
}

variable "force_destroy" {
  description = "Force destroy bucket with contents"
  type        = bool
  default     = true
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}
