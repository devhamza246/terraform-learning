# FastAPI Application Deployment with Terraform on Google Cloud Run

This project demonstrates how to deploy a FastAPI application using Terraform on Google Cloud Run.

## Overview

Google Cloud Run is a fully managed platform that automatically scales your containerized applications. Terraform is an infrastructure as code tool that allows you to define and provision infrastructure resources in a declarative way.

In this project, we use Terraform to provision the necessary infrastructure on Google Cloud Platform (GCP) and deploy a FastAPI application as a containerized service on Google Cloud Run.

## Project Structure

The project includes the following files:

- `main.tf`: Terraform configuration file defining the Google Cloud Run service.
- `Dockerfile`: Dockerfile for building the container image for the FastAPI application.
- `requirements.txt`: Python dependencies required for the FastAPI application.
- `main.py`: Main Python file containing the FastAPI application code.
- `README.md`: This README file providing an overview of the project.

## Prerequisites

Before running the deployment, ensure you have the following prerequisites:

- Google Cloud Platform account
- Google Cloud SDK installed locally
- Docker installed locally
- Terraform installed locally

## Deployment Steps

To deploy the FastAPI application on Google Cloud Run, follow these steps:

1. Authenticate with Google Cloud Platform:

    ```bash
    gcloud auth login
    ```

2. Initialize Terraform:

    ```bash
    terraform init
    ```

3. Plan the infrastructure changes:

    ```bash
    terraform plan
    ```

4. Apply the Terraform configuration:

    ```bash
    terraform apply
    ```

5. Build the Docker image:

    ```bash
    docker build -t gcr.io/your-project-id/fastapi-app .
    ```

6. Push the Docker image to Google Container Registry (GCR):

    ```bash
    docker push gcr.io/your-project-id/fastapi-app
    ```

7. Access the Cloud Run service URL:

    The Cloud Run service URL will be displayed in the Terraform output after successful deployment. You can also find it in the Google Cloud Console under the Cloud Run section.

## Testing

To test the deployed FastAPI application, you can send HTTP requests to the Cloud Run service URL using tools like cURL, Postman, or a web browser.

## Cleanup

To avoid incurring unnecessary charges, make sure to clean up the resources after testing:

1. Remove the Cloud Run service:

    ```bash
    terraform destroy
    ```

2. Delete the container image from Google Container Registry (optional):

    ```bash
    gcloud container images delete gcr.io/your-project-id/fastapi-app
    ```

## Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Terraform Documentation](https://learn.hashicorp.com/tutorials/terraform/google-cloud-run)

