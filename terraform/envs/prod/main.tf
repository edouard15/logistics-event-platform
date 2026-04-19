provider "aws" {
  region = var.region
}

module "vpc" {
  source = "../../modules/vpc"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"
}

module "iam" {
  source = "../../modules/iam"

  cluster_role_name = "prod-eks-cluster-role"
  node_role_name    = "prod-eks-node-role"
}
module "eks" {
  source = "../../modules/eks"

  cluster_name       = "prod-eks-cluster"
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnets

  cluster_role_arn = module.iam.cluster_role_arn
  node_role_arn    = module.iam.node_role_arn
}
