# Deploy Tensorflow serving model with Local Kubernetes Cluster

To deploy Tensorflow serving model with Local Kubernetes Cluster, This will implpement with `Kind`.

[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”.
kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

## Create Kubernetes single node cluster with Kind

To see how to install `Kind` [link](https://kind.sigs.k8s.io/docs/user/quick-start/)

```bash
kind create cluster
```

Run this command after create cluster to see kubernetes node:

```bash
kubectl get node
```

To deploy Tensorflow sreving in to Kubernetes cluster, run this command:

```bash
kubectl apply -f ./kube-config-local
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
        image: beans-model-gateway:v01
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

In order to connect to the Kubernetes cluster for testing the model serving. Expose port inside the Kubernetes cluster to outside port in the local computer run the command:

```bash
kubectl port-forward <kubernetes_service> <local_port>:<kubernetes_port>
```

Test with the following file:

```bash
python test.py
```

```python
import requests

# url = "http://localhost:9696/predict" # Test model gateway
url = "http://localhost:8080/predict" # Test model serving

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
