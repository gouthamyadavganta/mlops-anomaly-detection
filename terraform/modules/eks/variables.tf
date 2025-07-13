variable "project_name" {}
variable "environment" {}
variable "cluster_name" {}
variable "vpc_id" {}
variable "private_subnet_ids" {
  type = list(string)
}
variable "node_group_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}
variable "min_size" {
  type    = number
  default = 1
}
variable "max_size" {
  type    = number
  default = 3
}
variable "desired_size" {
  type    = number
  default = 2
}
variable "eks_node_role_arn" {
  type        = string
  description = "IAM role ARN for EKS node group"
}

