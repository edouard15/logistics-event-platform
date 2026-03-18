# Logistics FastAPI Microservices

## Description
Microservices-based logistics system using FastAPI, Docker, and Kubernetes.

## Services
- Order Service
- Tracking Service
- API Gateway

## Build Images

docker build -t edouard15/order-service ./order-service
docker build -t edouard15/tracking-service ./tracking-service
docker build -t edouard15/api-gateway ./api-gateway

## Deploy to Kubernetes

kubectl apply -f k8s/

## Access

http://<NODE-IP>:30007/track/123
