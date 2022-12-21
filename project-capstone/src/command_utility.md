# Command line utility

## Convert tf-serving.ipynb to scrtip

```bash
!jupyter nbconvert --to script tf-serving.ipynb
```

## Install AWS CLI

```bash
sudo apt install aws-cli
```

### Configure the profile by following command and put the credentials and configs

```bash
aws configure
```

## Run Docker container with Tensorflow Serving

```bash
docker run -it --rm \
    -p 8500:8500 \
    -v "$(pwd)/beans-model:/model/beans-model/1" \
    -e MODEL_NAME="beans-model" \
    tensorflow/serving:2.7.0
```

## Build docker image that by model_serving.dockerfile

```bash
docker build -t beans-model:xception_final_model -f model-serving.dockerfile .
```

## Run docker container that build from model_serving.dockerfile

```bash
docker run -it --rm \
-p 8500:8500 \
beans-model:xception_final_model
```

## Build docker image that by model_gateway.dockerfile

```bash
docker build -t beans-model-gateway:v01 -f model-gateway.dockerfile .
```

## Run docker container that build from model_gateway.dockerfile

```bash
docker run -it --rm \
-p 9696:9696 \
beans-model-gateway:v01
```

## Build docker image for application in side app folder

```bash
docker build -t bean-classifcation-app:v01 .
```

## Run docker container with bean-classification image

```bash
docker run -it --rm \
-p 8501:8501 \
bean-classification-app:v01
```

## Kind load docker image in cluster

```bash
kind load docker-image <image_name>
```

## Run Docker-compose from docker-compose.yaml

```bash
docker-compose up
```

**NOTE**: Make sure the `docker-compose.yaml` existing in the current directory

## Create Kubernetes single node cluster with Kind

To see how to install `kind` [link](https://kind.sigs.k8s.io/docs/user/quick-start/)

```bash
kind create cluster
```

## To see the services in the cluster

```bash
kubectl get pod,deploy,svc
```

## Deploy services in the Kubernetes local cluster

```bash
kubectl apply -f ./kube-config-local
```

```bash
kubectl port-forward <service> <port:port>
```

## Public the docker image of tf-serving gateway and service to `ECR`

### Create Elastic Container Registry

```bash
aws ecr create-repository --repository-name tf-serving-img
```

```bash
ACCOUNT_ID=551011018709
REGION=us-west-1
REGISTRY_NAME=tf-serving-img
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}
```

### Tag the serving app to push

```bash
APP_LOCAL=bean-classification-app:v01
APP_REMOTE=${PREFIX}:bean-classification-app-v01
docker tag ${APP_LOCAL} ${APP_REMOTE}
```

### Tag the model gateway remote to push

```bash
GATEWAY_LOCAL=beans-model-gateway:v02
GATEWAY_REMOTE=${PREFIX}:beans-model-gateway-v02
docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}
```

### Tag the model serving remote to push

```bash
SERVING_LOCAL=beans-model:xception_final_model
SERVING_REMOTE=${PREFIX}:beans-model-xception_final_model
docker tag ${SERVING_LOCAL} ${SERVING_REMOTE}
```

### Login to Elastin Container Registry

```bash
$(aws ecr get-login --no-include-email --region us-west-1)
```

**NOTE**: FIX THIS `denied: Your authorization token has expired. Reauthenticate and try again.` BY RUN THIS 

```bash
aws ecr get-login-password |docker login --username AWS --password-stdin $IMAGE_PATH
```

### Push the application to `ECR`

```bash
docker push ${APP_REMOTE}
```

### Push the model gateway service to `ECR`

```bash
docker push ${GATEWAY_REMOTE}
```

### Push the model serving service to `ECR`

```bash
docker push ${SERVING_REMOTE}
```

## Deploy services with the Elastic Kubernetes Service with `EKSCTL`

To see how to install `eksctl` [link](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)

```bash
wget https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz | tar xzfv eksctl_Linux_amd64.tag.gz
```

### Crate eks cluster

```bash
eksctl create cluster -f ./kube-config-eks/eks-config.yaml
```

```bash
kubectl apply -f ./kube-config-eks/
```

```bash
kubectl get svc
```

### Port for-ward in case of testing without External Loadbalancer

Forward model gateway with port `8500:8500`

```bash
kubectl port-forward beans-model-gateway 8500:8500
```

Forward model model serving with port `8080:80`

```bash
kubectl port-forward tf-serving-beans-model 8080:80
```

**NOTE**: Following the below instruciton in case `kubectl` cannot connect with `EKS` cluster

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update
```

## Save model to AWS S3

```bash
aws s3 cp <source> <target> --recursive
```

## Terraform installation see the [link](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
