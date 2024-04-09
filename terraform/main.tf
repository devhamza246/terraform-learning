# Create a Cloud Run service
resource "google_cloud_run_service" "fastapi_service" {
    name = "fastapi-app"
    location  = "us-central1"


    template {
    spec {
      containers {
        image = "gcr.io/terraform-learning-419716/terraform-learning:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Optional: Grant access to Cloud Run service (replace with your IAM role)
resource "google_cloud_run_service_iam_member" "allow_all_users" {
    service = google_cloud_run_service.fastapi_service.name
    role    = "roles/run.invoker"
    member  = "allUsers"
}
