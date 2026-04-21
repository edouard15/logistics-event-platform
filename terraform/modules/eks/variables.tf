variable "cluster_name" {}
variable "vpc_id" {}
variable "private_subnet_ids" {
  type = list(string)
}
variable "cluster_role_arn" {}
variable "node_role_arn" {}
