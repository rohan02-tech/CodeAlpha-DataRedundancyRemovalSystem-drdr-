output "storage_bucket_name" {
  description = "Chunk-store"
  value       = google_storage_bucket.chunk_store.name
}

output "spanner_instance_name" {
  description = "drdr-spanner-instance"
  value       = google_spanner_instance.main.name
}

output "pubsub_topic_name" {
  description = "chunk-processing-topic"
  value       = google_pubsub_topic.chunk_processing.name
}

output "service_account_email" {
  description = "rohanraj7999@gmail.com"
  value       = google_service_account.drdr_worker.email
}
