provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# ---------------- PROMETHEUS + ALERTMANAGER ----------------
resource "helm_release" "prometheus" {
  name             = "kube-prometheus"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true

  values = [file("${path.module}/values/prometheus.yaml")]
}

# ---------------- ELASTICSEARCH ----------------
resource "helm_release" "elasticsearch" {
  name             = "elasticsearch"
  repository       = "https://helm.elastic.co"
  chart            = "elasticsearch"
  namespace        = "logging"
  create_namespace = true
}

# ---------------- KIBANA ----------------
resource "helm_release" "kibana" {
  name       = "kibana"
  repository = "https://helm.elastic.co"
  chart      = "kibana"
  namespace  = "logging"
}

# ---------------- FLUENT BIT (REPLACES FLUENTD) ----------------
resource "helm_release" "fluentbit" {
  name       = "fluent-bit"
  repository = "https://fluent.github.io/helm-charts"
  chart      = "fluent-bit"
  namespace  = "logging"

  values = [file("${path.module}/values/fluentbit.yaml")]
}

# ---------------- JAEGER ----------------
resource "helm_release" "jaeger" {
  name             = "jaeger"
  repository       = "https://jaegertracing.github.io/helm-charts"
  chart            = "jaeger"
  namespace        = "observability"
  create_namespace = true

  values = [file("${path.module}/values/jaeger.yaml")]
}
