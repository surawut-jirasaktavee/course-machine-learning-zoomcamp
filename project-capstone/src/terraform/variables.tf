# Define the local variables
locals {
  tags = {
    Name        = "model-serving"
    Environment = "production"
    Team        = "model-serving"
  }

  region  = "us-west-2"
  profile = "default"
}

variable "eks_cluster_name" {
  type        = string
  default     = "tf-serving-cluster"
  description = "Name of AWS Elastic Kubernetes Service cluster"
}
