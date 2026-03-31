# Logistics Event Processing Microservices

## Overview
Cloud-native logistics microservices system built with FastAPI, Docker, and Kubernetes (Minikube).

Simulates real-world delivery workflows such as order management and shipment tracking using a scalable microservices architecture.

---

## Architecture

- API Gateway (entry point for external requests)
- Order Service (handles order creation)
- Tracking Service (handles shipment tracking)

Each service is containerized and deployed on Kubernetes with multiple replicas.

---

## Tech Stack

- FastAPI (Python microservices)
- Docker (containerization)
- Kubernetes (Minikube for orchestration)
- REST APIs with Swagger UI documentation

---

## Kubernetes Deployment (Working Setup)

### Running Pods

```bash
kubectl get pods
