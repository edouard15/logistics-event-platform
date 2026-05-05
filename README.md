# Logistics Microservices Platform on AWS EKS (CI/CD + Observability)

## Overview
Cloud-native **logistics microservices system** deployed on AWS EKS with full CI/CD and observability stack.

Services:
- API Gateway
- Order Service
- Tracking Service

---

## Architecture

- Kubernetes (EKS)
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)

Observability:
- Metrics → Prometheus
- Logs → Fluent Bit + Elasticsearch + Kibana
- Traces → OpenTelemetry + Jaeger

---

## CI/CD Pipeline

1. Code Quality (flake8, black, pytest)
2. Build & Push Docker images
3. Terraform Plan & Apply
4. Deploy to EKS
5. Observability validation

---

## Domain Flow

Order → API Gateway → Order Service → Tracking Service

---

## Access

```text id="a8m2qz"
http://api.yourdomain.com
