# Logistics Microservices Platform — AWS EKS

![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-FastAPI-009688?logo=fastapi&logoColor=white)

A production-grade, cloud-native logistics platform built solo on AWS — from infrastructure provisioning to full observability. Designed to reflect real-world delivery workflows: order intake, routing, and shipment tracking across distributed microservices.

---

## Why I Built This

Most DevOps portfolios deploy a generic "todo app." I spent 5 years in logistics operations at Knight-Swift Transportation — I know what these systems look like from the inside, where they fail, and what reliability actually costs.

This project applies cloud-native engineering to a domain I understand deeply: a microservices platform that mirrors the architecture behind real freight and delivery systems.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Actions                      │
│   quality → build → tf-plan → approval → apply → deploy │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      AWS (us-east-1)                    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  VPC                             │   │
│  │                                                  │   │
│  │   ┌────────────┐     ┌──────────────────────┐   │   │
│  │   │    EKS     │     │      Terraform        │   │   │
│  │   │  Cluster   │     │  S3 backend +         │   │   │
│  │   │            │     │  DynamoDB locking     │   │   │
│  │   │ ┌────────┐ │     └──────────────────────┘   │   │
│  │   │ │  API   │ │                                  │   │
│  │   │ │Gateway │ │     ┌──────────────────────┐   │   │
│  │   │ └───┬────┘ │     │    Observability      │   │   │
│  │   │     │      │     │                       │   │   │
│  │   │ ┌───▼────┐ │     │  Prometheus (metrics) │   │   │
│  │   │ │ Order  │ │     │  EFK stack (logs)     │   │   │
│  │   │ │Service │ │     │  Jaeger + OTEL (trace)│   │   │
│  │   │ └───┬────┘ │     └──────────────────────┘   │   │
│  │   │     │      │                                  │   │
│  │   │ ┌───▼────┐ │                                  │   │
│  │   │ │Tracking│ │                                  │   │
│  │   │ │Service │ │                                  │   │
│  │   │ └────────┘ │                                  │   │
│  │   └────────────┘                                  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Request flow:** `Client → API Gateway → Order Service → Tracking Service`

---

## Services

| Service | Description | Port |
|---|---|---|
| `api-gateway` | Entry point — routes requests, handles auth | 8000 |
| `order-service` | Manages order creation and state | 8001 |
| `tracking-service` | Handles shipment tracking and status updates | 8002 |

All services built with **FastAPI** and containerized with **Docker**. Images tagged with Git SHA for immutable, traceable deployments.

---

## Infrastructure (Terraform)

```
terraform/
├── envs/
│   └── prod/          # Production environment config
├── modules/
│   ├── vpc/           # VPC, subnets, routing
│   ├── eks/           # EKS cluster + node groups
│   └── iam/           # Least-privilege IAM roles
```

**Key design decisions:**
- Remote state in S3 with DynamoDB locking — no state conflicts in CI
- OIDC-based GitHub Actions → AWS auth — zero static credentials stored anywhere
- Modular structure — drop in a `staging/` env without touching module code

---

## CI/CD Pipeline (6 Stages)

```
push to master
      │
      ▼
┌─────────────┐
│   quality   │  flake8 lint + black format + pytest (per service)
└──────┬──────┘
       ▼
┌─────────────┐
│    build    │  Docker build + push to registry (tagged with git SHA)
└──────┬──────┘
       ▼
┌─────────────┐
│  tf-plan    │  terraform init → validate → plan (artifact uploaded)
└──────┬──────┘
       ▼
┌─────────────┐
│  approval   │  Manual gate — human reviews plan before infra changes
└──────┬──────┘
       ▼
┌─────────────┐
│  tf-apply   │  Downloads plan artifact → applies exact reviewed plan
└──────┬──────┘
       ▼
┌─────────────┐
│   deploy    │  kubectl apply → image update → rollout status check
└──────┬──────┘
       ▼
┌──────────────────┐
│ observability    │  Verify monitoring/logging/tracing pods + /metrics
│ check            │  Generate 100 synthetic requests → validate stack
└──────────────────┘
```

**Security highlights:**
- AWS auth via OIDC (no secrets in CI)
- Manual approval gate before every production infrastructure change
- Immutable image tags — every deploy is fully traceable to a commit

---

## Observability Stack

| Signal | Tool | Namespace |
|---|---|---|
| Metrics | Prometheus | `monitoring` |
| Logs | Fluent Bit + Elasticsearch + Kibana | `logging` |
| Traces | OpenTelemetry + Jaeger | `observability` |

Post-deploy, the pipeline automatically:
1. Verifies all observability pods are running
2. Generates 100 synthetic requests across all endpoints
3. Validates the `/metrics` endpoint is serving Prometheus data

---

## Repository Structure

```
.
├── api-gateway/          # FastAPI gateway service
├── order-service/        # FastAPI order service
├── tracking-service/     # FastAPI tracking service
├── k8s/                  # Kubernetes manifests
├── terraform/
│   ├── envs/prod/        # Production Terraform config
│   └── modules/          # Reusable Terraform modules
└── .github/
    └── workflows/
        └── pipeline.yml  # Full CI/CD pipeline
```

---

## Local Development

```bash
# Clone the repo
git clone https://github.com/edouard15/logistics-event-platform.git
cd logistics-event-platform

# Run all services locally
docker compose up --build

# Run tests
pytest order-service -v
pytest tracking-service -v
pytest api-gateway -v
```

---

## Key Engineering Decisions

**Why OIDC over AWS access keys?**
Static credentials in CI are a common attack vector. OIDC lets GitHub Actions assume an IAM role directly — no long-lived secrets stored anywhere.

**Why a manual approval gate?**
Terraform apply is destructive. An automated apply on every push is how you accidentally delete a production database. The approval gate enforces human review of the plan artifact before any infrastructure changes land.

**Why separate observability namespaces?**
Isolating monitoring, logging, and tracing into dedicated namespaces (`monitoring`, `logging`, `observability`) prevents resource contention, simplifies RBAC, and makes it easy to upgrade or replace individual components without touching others.

---

## Background

This project was deliberately built around logistics — a domain I operated in for 5+ years. I understand the reliability requirements of freight systems not just from an engineering perspective, but from having been on the operational side when things go wrong.

That context shapes how I build: observability-first, failure-tolerant, and with a bias toward systems that hold up under real-world pressure.

---

*Built by Edouard Akotonou· [LinkedIn] https://www.linkedin.com/in/edouard-akotonou-8487873b9/ · CKA Candidate*
