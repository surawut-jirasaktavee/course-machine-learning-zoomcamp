# provider "kubernetes" {
#   version = "~> 1.11"
#   alias   = "eks"

#   # Configure the provider to use the EKS cluster
#   cluster_ca_certificate = base64decode(aws_eks_cluster.eks_cluster.certificate_authority.0.data)
#   host                   = aws_eks_cluster.eks_cluster.endpoint
#   token                  = data.aws_eks_cluster_auth.eks_cluster_auth.token
# }

# data "aws_eks_cluster_auth" "eks_cluster_auth" {
#   name = aws_eks_cluster.eks_cluster.name
# }

# # Apply the model-serving-deployment.yaml file to the EKS cluster
# resource "kubernetes_manifest" "deployment1" {
#   provider = kubernetes.eks

#   manifest = file("../kube-config-eks/model-serving-deployment.yaml")
# }

# # Apply the model-gateway-deployment.yaml file to the EKS cluster
# resource "kubernetes_manifest" "deployment2" {
#   provider = kubernetes.eks

#   manifest = file("../kube-config-eks/model-gateway-deployment.yaml")
# }

# # Apply the model-serving-service.yaml file to the EKS
# resource "kubernetes_manifest" "deployment1" {
#   provider = kubernetes.eks

#   manifest = file("../kube-config-eks/model-serving-service.yaml")
# }

# # Apply the model-gateway-service.yaml file to the EKS
# resource "kubernetes_manifest" "deployment1" {
#   provider = kubernetes.eks

#   manifest = file("../kube-config-eks/model-gateway-service.yaml")
# }
