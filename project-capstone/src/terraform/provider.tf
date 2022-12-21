terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4.40.0"
    }
  }
}

provider "aws" {
  profile = local.profile
  region  = local.region
}