provider "google" {
  credentials = file("key.json")
  project     = "terraform-learning-419716"
  region      = "us-central1"
}