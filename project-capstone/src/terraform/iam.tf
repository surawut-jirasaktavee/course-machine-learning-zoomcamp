# Create an IAM policy for the EKS cluster
resource "aws_iam_policy" "eks_policy" {
  name        = "eks_policy"
  description = "IAM policy for EKS cluster"
  policy      = file("eks_cluster_policy.json")
  tags        = local.tags
}

# Create an IAM role for the EKS cluster
resource "aws_iam_role" "eks_role" {
  name               = "eks_role"
  assume_role_policy = file("eks_role_policy.json")
  tags               = local.tags
}

# Create the ECR policy
resource "aws_iam_policy" "ecr_policy" {
  name   = "ecr_policy"
  policy = file("ecr_policy.json")
  tags   = local.tags
}

# Attach the ECR policy to the EKS node group's IAM role
resource "aws_iam_policy_attachment" "ecr_policy_attachment" {
  name       = "ecr_policy_attachment"
  policy_arn = aws_iam_policy.ecr_policy.arn
  roles      = [aws_iam_role.eks_node_role.name]
}


resource "aws_iam_role" "eks_node_role" {
  name               = "eks_node_role"
  assume_role_policy = file("eks_node_policy.json")
  tags               = local.tags
}


# Attach the IAM policy to the IAM role
resource "aws_iam_policy_attachment" "eks_policy_attachment1" {
  name       = "eks_policy_attachment"
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  roles      = [aws_iam_role.eks_role.name]
}

resource "aws_iam_policy_attachment" "eks_worker_node_policy" {
  name       = "attach-eks-worker-node-policy"
  roles      = [aws_iam_role.eks_node_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_policy_attachment" "ecr_readonly_policy" {
  name       = "attach-ecr-readonly-policy"
  roles      = [aws_iam_role.eks_node_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
