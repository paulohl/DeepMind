# Once pushed, the fully generated path (${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG}) 
# becomes the absolute string value provided to the container_uri argument inside deploy.py orchestration pipeline.

# 1. Define deployment parameters
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
REPO_NAME="cyber-control-plane-repo"
IMAGE_NAME="policy-gate-inference"
TAG="latest"

# 2. Authenticate local Docker daemon with GCP Artifact Registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# 3. Create the Docker Repository in Artifact Registry (run once)
gcloud artifacts repositories create ${REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Autonomous Control Plane Secure Images"

# 4. Build the Docker image matching target cloud architecture
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG} .

# 5. Push the compiled asset to Google Cloud
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG}
