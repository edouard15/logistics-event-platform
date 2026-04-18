
# Create EKS Cluster
resource "aws_eks_cluster" "logistics" {
  name     = "logistics"
  role_arn = data.terraform_remote_state.network.outputs.node_role

  vpc_config {
    subnet_ids = [
      data.terraform_remote_state.network.outputs.public[0], data.terraform_remote_state.network.outputs.public[1],
      data.terraform_remote_state.network.outputs.private[0], data.terraform_remote_state.network.outputs.private[1]
    ]
  }
}
