

gcp-cognitive-control-plane/      
│      
├── .gitignore      
├── README.md      
│      
├── /edge_container/                 # WORLD 1: The runtime policy middleware      
│   ├── app.py                       # The FastAPI policy gate and Lipschitz drift checks      
│   ├── Dockerfile                   # Packages app.py for Artifact Registry      
│   └── requirements.txt             # (fastapi, uvicorn, pydantic, google-cloud-aiplatform)      
│      
├── /infrastructure/                 # WORLD 2: Vertex AI Orchestration & CI/CD      
│   ├── deploy.py                    # Python script to provision the Vertex AI Endpoint      
│   └── cloudbuild.yaml              # The CI/CD pipeline that compiles the container      
│      
└── /tripwire_function/              # WORLD 3: The automated intervention circuit breaker      
    ├── main.py                      # Google Cloud Function script parsing Pub/Sub alerts      
    └── requirements.txt             # (functions-framework, google-cloud-aiplatform)      
