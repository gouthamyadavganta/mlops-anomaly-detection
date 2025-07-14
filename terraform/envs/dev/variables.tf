variable "aws_region" {
  default = "us-east-2"
}

variable "project_name" {
  default = "mlops-anomaly"
}

variable "environment" {
  default = "dev"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "desired_size" {
  default = 2
}
variable "min_size" {
  default = 1
}
variable "max_size" {
  default = 3
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  default     = "mlops-anomaly-dev-eks"
}

variable "ssh_key_name" {
  description = "Name of the EC2 Key Pair to SSH into EKS nodes"
  default     = "devops project1"
}
