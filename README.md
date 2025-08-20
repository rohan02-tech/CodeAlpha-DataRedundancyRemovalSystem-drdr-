# DataRedundancyRemovalSystem drdr Cloud System

A cloud-native Data Redundancy Removal system built on Google Cloud Platform (GCP).

## Architecture

This system uses a microservices architecture to provide scalable and efficient deduplication.

**Core Components:**
- **Upload Service (Cloud Run):** Accepts file uploads, performs chunking, and checks for existing chunks.
- **Storage Worker (Cloud Run):** Asynchronously processes unique chunks (Pub/Sub) and stores them in Cloud Storage.
- **Metadata Storage:** Firestore (file manifests) and Cloud Spanner (global chunk index).
- **Chunk Storage:** Google Cloud Storage.

## Quick Start

### Prerequisites
- Google Cloud Project with billing enabled
- Terraform >= 1.0
- Google Cloud CLI installed and configured

### Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/drdr-cloud-system.git
   cd drdr-cloud-system
