# The Execution Sequence

The deployment sequence moves entirely into the automated cloud:      

* *Connect to GCP*: You will link this GitHub repository directly to Google Cloud Build.
* *The Trigger*: The moment you push a commit to the main branch, Cloud Build reads your cloudbuild.yaml file.
* ^The Automated Build*: Cloud Build securely compiles the /edge_container code into a Docker image, tags it, and pushes it to your Google Cloud Artifact Registry.
* *The Deployment*: You (or a subsequent pipeline step) run deploy.py to pull that newly minted image and launch it onto the TPU-backed Vertex AI Endpoint.

