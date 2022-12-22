# Deploy Tensorflow serving model with AWS Elastic Kubernetes Service

To deploy Tensorflow serving model with Cloud provider Kubernetes Cluster, This will implpement with `AWS EKS`.

[Amazon EKS](https://aws.amazon.com/eks/) is a managed Kubernetes service to run Kubernetes in the AWS cloud and on-premises data centers. In the cloud, Amazon EKS automatically manages the availability and scalability of the Kubernetes control plane nodes responsible for scheduling containers, managing application availability, storing cluster data, and other key tasks.

## Software requirements

- awscli
- kubectl
- eksctl
- AWS ECR

### AWSCLI installation

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update
```

#### Configuration `AWSCLI` to connect to AWS

Run the following command to configure the AWS credentials and configurations.

```bash
aws configure
```

### KUBECTL installation

See the [documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

### EKSCTL installation

In order to To see how to install `eksctl` see the [link](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html) or follow the following instructions:

```bash
wget https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz | tar xzfv eksctl_Linux_amd64.tag.gz
```

### AWS ECR see the [instructions](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/instruction/aws_ecr.md)

## Deployment

### Create Kubernetes cluster with `eksctl`

```bash
eksctl create cluster -f ./kube-config-eks/eks-config.yaml
```

![](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/images/aws_eks.png)

```eks-config.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: tf-serving-eks
  region: us-west-1
nodeGroups:
  - name: tf-serving-node-group-m5-xlarge
    instanceType: m5.xlarge
    desiredCapacity: 2
```

Run this command after create cluster to see kubernetes node:

```bash
kubectl get node
```

To deploy Tensorflow sreving in to Kubernetes cluster, run this command:

```bash
kubectl apply -f ./kube-config-eks
```

It depends on the current working directory. If you are inside `kube-config-local` directory you will need to run file by file. For example:

```bash
kubectl apply -f ./kube-config-local/model-gateway-deploy.yaml
kubectl apply -f ./kube-config-local/model-gateway.service.yaml
```

model-gateway-deploy.yaml file:

```model-gateway-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: beans-model-gateway
spec:
  selector:
    matchLabels:
      app: beans-model-gateway
  template:
    metadata:
      labels:
        app: beans-model-gateway
    spec:
      containers:
      - name: beans-model-gateway
        image: 551011018709.dkr.ecr.us-west-1.amazonaws.com/tf-serving-img:beans-model-gateway-v02
        resources:
          limits:
            memory: "512Mi"
            cpu: "1024m"
        ports:
        - containerPort: 9696
        env:
          - name: TF_SERVING_HOST
            value: tf-serving-beans-model.default.svc.cluster.local:8500

```

model-gateway-service.yaml file:

```model-gateway.service.yaml
apiVersion: v1
kind: Service
metadata:
  name: beans-model-gateway
spec:
  type: LoadBalancer
  selector:
    app: beans-model-gateway
  ports:
  - port: 80
    targetPort: 9696
```

See the service inside Kubernetes cluster:

```bash
kubectl get pod,deploy,svc
```

![](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/images/aws_eks_pod.png)

Test with the following file:

```bash
python test.py
```

```python
import requests

url = "" # Put the url of External Load Balancer of the service

# source images
# https://huggingface.co/datasets/beans/viewer/default/test

# Healthy
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/98/image/image.jpg"

# Bean rust
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/84/image/image.jpg"

# Angular_leaf_spot
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/24/image/image.jpg"

data = {
    "url": "https://datasets-server.huggingface.co/assets/beans/--/default/test/84/image/image.jpg"
}

result = requests.post(url, json=data).json()
print(result)
```
