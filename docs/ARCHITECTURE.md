# DRDR Cloud System Architecture

## Overview
A cloud-native Data Redundancy Removal system built on Google Cloud Platform.

## Components

### 1. Upload Service (Cloud Run)
- Accepts file uploads via HTTP
- Performs content-defined chunking
- Checks chunk existence in Spanner
- Publishes unique chunks to Pub/Sub

### 2. Storage Worker (Cloud Run)
- Subscribes to Pub/Sub topics
- Stores chunks in Cloud Storage
- Updates Spanner metadata
- Handles compression/encryption

### 3. Data Storage
- **Cloud Storage**: Chunk object storage
- **Spanner**: Global chunk index
- **Firestore**: File manifests and metadata

### 4. Infrastructure
- Terraform-managed resources
- Automated CI/CD with GitHub Actions
- IAM and security policies
