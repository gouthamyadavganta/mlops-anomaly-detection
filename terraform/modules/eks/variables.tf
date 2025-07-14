variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

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

variable "ssh_key_name" {
  type        = string
  description = "EC2 key pair name for SSH access to nodes"
}

