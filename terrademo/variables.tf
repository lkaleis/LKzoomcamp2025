variable "credentials" {
  description = "my credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "neon-runway-447221-q8"
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "storage bucket name"
  default     = "neon-runway-447221-q8-terra-bucket"
}

variable "location" {
  description = "proj location"
  default     = "northamerica-northeast2"
}

variable "region" {
  description = "proj region"
  default     = "northamerica-northeast2"
}