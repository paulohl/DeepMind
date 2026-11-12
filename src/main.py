import base64
import json
import logging
import functions_framework
from google.cloud import aiplatform

# Configure industrial log formatting
logging.basicConfig(level=logging.INFO)

def invoke_targeted_intervention_pipeline(project_id: str, region: str, endpoint_id: str, anomaly_score: float):
    """ 
    Triggers the Section 4 Targeted Intervention Loop via Vertex AI Pipelines. 
    Re-routes adversarial traffic and runs automated model fine-tuning. 
    """
    aiplatform.init(project=project_id, location=region)

    # Target execution parameters matching Chapter 11 specifications
    pipeline_spec_uri = f"https://googleapis.com{project_id}-pipeline-bucket/intervention_loop.json"

    parameter_payload = {
        "drift_endpoint": endpoint_id,
        "empirical_anomaly_score": anomaly_score,
        "fallback_strategy": "GEMINI_2_5_FLASH_CIRCULATION"
    }

    logging.info(f"[Tripwire Active] Launching Vertex Pipeline execution from: {pipeline_spec_uri}")

    # Fire-and-forget orchestration execution
    job = aiplatform.PipelineJob(
        display_name="autonomous-intervention-circuit-break",
        template_path=pipeline_spec_uri,
        pipeline_root=f"gs://{project_id}-pipeline-bucket/runs/",
        parameter_values=parameter_payload
    )
    job.submit()
    logging.info(f"[Tripwire Settled] Pipeline job submitted successfully: {job.resource_name}")

@functions_framework.cloud_event
def parse_vertex_monitoring_alert(cloud_event):
    """ 
    Cloud Function Gen 2 Entry Point. 
    Listens to a Pub/Sub topic streaming Vertex AI Model Monitoring alerts. 
    """
    # 1. Decode the secure Pub/Sub payload data
    try:
        pubsub_message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        alert_payload = json.loads(pubsub_message)
        logging.info(f"Ingested alert stream payload from Vertex AI Monitor.")
        
        # 2. Extract anomaly details and trigger intervention (Integration bridge)
        endpoint_id = alert_payload.get("endpoint_id", "unknown-endpoint")
        anomaly_score = alert_payload.get("anomaly_score", 1.0)
        
        # 3. Invoke the execution pipeline
        invoke_targeted_intervention_pipeline(
            project_id="cyber-control-plane", 
            region="us-central1", 
            endpoint_id=endpoint_id, 
            anomaly_score=anomaly_score
        )
        
    except Exception as e:
        logging.error(f"Failed to decode inbound message payload block: {str(e)}")
        return
