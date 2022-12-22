# AWS Elastic Container Registry Service

To store the image of the container that created to the `AWS Elastic Container Registry` follow the following steps:

## Public the docker image of tf-serving gateway and service to `ECR`

### Create Elastic Container Registry

```bash
aws ecr create-repository --repository-name <repository-name>
```

Set the following environment variables for pushing and pulling the docker image

```bash
ACCOUNT_ID=551011018709
REGION=us-west-1
REGISTRY_NAME=tf-serving-img
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}
```

Before push the image to the registry. Tag the image with the proper name and tag

### Tag the serving app to push

```bash
LOCAL_IMAGE=<local_image_name>:<local_tag>
REMOTE_IMAGE=${PREFIX}:<remote_tag>
docker tag ${APP_LOCAL} ${APP_REMOTE}
```

### Login to Elastin Container Registry

```bash
$(aws ecr get-login --no-include-email --region us-west-1)
```

**NOTE**: FIX THIS `denied: Your authorization token has expired. Reauthenticate and try again.` BY RUN THIS 

```bash
aws ecr get-login-password |docker login --username AWS --password-stdin $IMAGE_PATH
```

### Push the image to `ECR`

```bash
docker push ${REMOTE_IMAGE}
```
