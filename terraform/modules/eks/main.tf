module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.24"

  cluster_name = var.cluster_name

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_irsa = true

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  iam_role_arn = var.cluster_role_arn

  # ✅ Modern authentication (no aws-auth)
  authentication_mode = "API"

  eks_managed_node_groups = {
    default = {
      desired_size = 2
      min_size     = 2
      max_size     = 5

      instance_types = ["t3.medium"]
      iam_role_arn   = var.node_role_arn
    }
  }

  # ✅ Access entries (IAM-based access control)
  access_entries = {
    github = {
      principal_arn = "arn:aws:iam::909614386406:role/Github-Actions"

      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

          access_scope = {
            type = "cluster"
          }
        }
      }
    }

    local = {
      principal_arn = "arn:aws:iam::909614386406:role/EKS-Local-Admin"

      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }
}
