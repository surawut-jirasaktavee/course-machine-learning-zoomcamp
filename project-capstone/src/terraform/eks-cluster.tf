# Create an EKS cluster
resource "aws_eks_cluster" "eks_cluster" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks_role.arn
  vpc_config {
    subnet_ids = [
      aws_subnet.eks_public_subnet_1.id,
      aws_subnet.eks_public_subnet_2.id,
    ]
  }
  tags = local.tags
}

resource "aws_eks_node_group" "eks_node_group" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "m5-xlarge-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  scaling_config {
    min_size     = 2
    max_size     = 2
    desired_size = 2
  }
  instance_types = ["m5.xlarge"]
  subnet_ids     = [aws_subnet.eks_public_subnet_1.id, aws_subnet.eks_public_subnet_2.id]
}
