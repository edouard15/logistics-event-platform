module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.4"

  cluster_name = var.cluster_name

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_irsa = true

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  iam_role_arn = var.cluster_role_arn

  eks_managed_node_groups = {
    default = {
      desired_size = 2
      min_size     = 2
      max_size     = 5

      instance_types = ["t3.medium"]

      iam_role_arn = var.node_role_arn
    }
  }
}
