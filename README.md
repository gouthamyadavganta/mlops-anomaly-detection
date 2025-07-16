# Real-Time Anomaly Detection MLOps System

## Overview

This project demonstrates a **production-ready, cloud-native MLOps pipeline** that automates the full lifecycle of a real-time anomaly detection model using modern DevOps, GitOps, and ML tooling. It is designed to:

- Showcase end-to-end MLOps expertise to recruiters, engineers, and hiring managers
- Automate everything from training to deployment using CI/CD and GitHub Actions
- Enable retraining and redeployment based on drift detection
- Integrate observability and multi-layer security scanning
- Use only scalable, industry-standard, cloud-native tools

---

## 🧰 Tech Stack

| Category          | Tool                            | Usage |
|------------------|----------------------------------|-------|
| Cloud             | AWS (EKS, S3, IAM, VPC)          | Hosting, storage, roles |
| IaC               | Terraform                        | VPC, EKS, IAM, S3 (with remote backend) |
| CI/CD             | GitHub Actions                   | Model training, image build, chart publishing |
| GitOps            | ArgoCD                           | Helm-based continuous delivery |
| ML/Serving        | IsolationForest + FastAPI        | Anomaly detection + REST API |
| Tracking          | MLflow + S3 + SQLite             | Logs metrics/artifacts, tracks versions |
| Containerization  | Docker + Docker Hub              | Build & registry |
| Monitoring        | Prometheus + Grafana             | Metrics, dashboards, alerts |
| Drift Detection   | Custom logic + CronJob           | Detects drift and triggers retraining |
| Security          | tfsec, TFLint, Trivy, CodeQL     | Infra, container, and code scanning |

---

## 📐 System Architecture

mermaid
graph TD
  subgraph CI/CD
    GH[GitHub Actions]
    ARGO[ArgoCD]
  end

  subgraph AWS Cloud
    TF[Terraform Infrastructure]
    EKS[Kubernetes Cluster (EKS)]
    MLFlow[MLflow Server]
    FastAPI[Inference API]
    Prometheus[Prometheus]
    Grafana[Grafana]
    Cron[CronJob - Drift Trigger]
    S3[S3 Buckets]
  end

  GH -->|Push / PRs| ARGO
  GH -->|Upload model + Helm| S3
  TF --> EKS
  FastAPI --> MLFlow
  FastAPI --> Prometheus
  Cron --> GH
  ARGO -->|Sync| EKS

graph TB
  VPC[VPC]
  Subnet1[Public Subnet]
  Subnet2[Private Subnet]
  IGW[Internet Gateway]
  NAT[NAT Gateway]
  EKS[EKS Cluster]
  NodeGroup[Managed Node Group]
  S3[S3 Buckets]
  Dynamo[DynamoDB State Lock]
  Terraform[Remote Backend]

  VPC --> Subnet1
  VPC --> Subnet2
  Subnet1 --> IGW
  Subnet2 --> NAT
  VPC --> EKS
  EKS --> NodeGroup
  Terraform --> S3
  Terraform --> Dynamo

🔄 End-to-End Pipeline
mermaid
CopyEdit
flowchart TD
  A[train-model.yml]
  B[MLflow Logging + Upload to S3]
  C[Create PR to update model.pkl in inference-api/]
  D[Merge triggers build-deploy.yml]
  E[Build + Push Docker Image to Docker Hub]
  F[Create PR to update image tag in Helm chart]
  G[Merge triggers upload-helm.yml]
  H[Upload Helm chart to S3 bucket]
  I[ArgoCD watches and syncs chart]
  J[Updated FastAPI inference deployed to EKS]

  A --> B --> C --> D --> E --> F --> G --> H --> I --> J
________________________________________
⚙️ CI/CD Workflows (Updated Table)
Workflow	Trigger	Purpose
terraform.yml	Push to terraform/** or manual dispatch	Plan infrastructure changes; apply only on manual approval
train-model.yml	Manual dispatch or model change	Trains IsolationForest model → Logs to MLflow + S3 → Creates PR to update model.pkl
build-deploy.yml	Push to services/inference-api/ or Helm chart	Builds + pushes Docker image → Creates PR to update Helm values.yaml
upload-helm.yml	Helm chart update	Uploads .tgz chart + index to S3 chart repo
security.yml	Every push or PR to main	Runs tfsec, TFLint, Trivy (image scan), and CodeQL (code scan)
________________________________________
📦 Breakdown of Workflow Responsibilities
✅ train-model.yml
•	Trains model with train.py
•	Logs metrics and saves model to S3 via MLflow
•	Creates a PR to update services/inference-api/model.pkl
✅ build-deploy.yml
•	Triggered when model.pkl or inference code changes
•	Builds/pushes image to Docker Hub
•	Opens PR to update Helm chart (tag: in values.yaml)
✅ upload-helm.yml
•	Triggered when Helm chart changes (e.g., after PR merge)
•	Packages chart, updates Helm index, and pushes to S3
✅ terraform.yml
•	Runs fmt, init, validate, plan on push
•	Applies infra only on manual trigger via workflow_dispatch
✅ security.yml
•	Scans:
o	Terraform (tfsec, tflint)
o	Docker image (trivy)
o	App code (CodeQL)
🛠️ Infrastructure with Terraform
•	Modular design under terraform/modules/
•	terraform/envs/dev/ uses:
o	S3: stores remote state
o	DynamoDB: locks state
•	Provisions:
o	VPC, subnets, NAT, IGW
o	IAM roles
o	EKS cluster + node group
o	S3 buckets for:
	model.pkl
	Helm charts
________________________________________
🚀 Deployment via ArgoCD + Helm
•	Helm charts are defined in helm/inference-api/
•	On image build, PR updates tag: in values.yaml
•	ArgoCD tracks argocd/inference-app.yaml
•	When Helm values update → ArgoCD syncs → new image deployed
________________________________________
🐳 Docker
•	Two Dockerfiles:
o	services/inference-api/
o	model/scripts/train.py
•	Images pushed to Docker Hub: gantagouthamyadav/inference-api
•	CI pipeline handles build & push
________________________________________
📂 Folder Structure
bash
CopyEdit
mlops-anomaly-detection/
├── .github/workflows/       # GitHub Actions: CI/CD, Security
├── argocd/                  # ArgoCD app manifest
├── helm/                    # Helm chart (FastAPI)
├── model/                   # Training pipeline
│   └── scripts/train.py
├── services/                # Inference API (FastAPI)
├── terraform/               # IaC (modular)
│   ├── modules/
│   └── envs/dev/
├── simulate_stream.py       # Mock streaming simulator
________________________________________
👥 Who This Project Is For
•	Recruiters/Hiring Managers: See real MLOps capability in action
•	Engineers: Explore scalable automation + GitOps patterns
•	Contributors: Extend or reuse modules in your own pipelines
________________________________________
✅ Results
•	Fully automated MLOps lifecycle
•	Drift triggers retraining via Cron + GitHub API
•	Container and infra security built in
•	Monitoring and alerting (Grafana, Prometheus)
•	Clean GitOps integration with ArgoCD + Helm
________________________________________
🧯 Troubleshooting
Area	Problem	Fix
MLflow	Upload fails to S3	Ensure AWS credentials via K8s Secret
ArgoCD	No sync/deployment	Check Helm chart PR merged & uploaded
Grafana	Can't log in	Reset Bitnami creds or recreate secret
CronJob	Not triggering	Check kubectl get cronjob -n mlops
GitHub	PR not created	Ensure GH_PAT secret is available
________________________________________
🧪 Local Testing (Optional)
bash
CopyEdit
# Clone the project
git clone https://github.com/<your-name>/mlops-anomaly-detection.git
cd mlops-anomaly-detection

# Run local model trainer (demo only)
python model/scripts/train.py

# Start FastAPI app
cd services/inference-api
uvicorn main:app --reload

# Simulate real-time input
python simulate_stream.py
________________________________________
🧠 What Can Be Improved
•	Add tests: pytest for FastAPI & model
•	Use IRSA for AWS access in cluster
•	Replace SQLite MLflow backend with RDS (MySQL/PostgreSQL)
•	Add Kafka/Kinesis for live streaming demo
•	Integrate a load test tool (e.g., Locust)
________________________________________
📚 References
•	Terraform
•	MLflow
•	FastAPI
•	ArgoCD
•	Prometheus
•	Grafana
•	Trivy
•	CodeQL    
