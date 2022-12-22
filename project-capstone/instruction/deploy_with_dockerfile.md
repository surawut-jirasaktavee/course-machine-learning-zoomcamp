# Deploy Tensorflow serving model with Docker image

To deploy the Tersorflow model I have created Docker images with 2 dockerfiles as following:

1. `model-gateway.dockerfile`

```dockerfile
FROM python:3.9.12-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["tf_serving_gateway2.py", "proto.py", "./"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "tf_serving_gateway2:app" ]
```

2. `model-serving.dockerfile`

```dockerfile
FROM tensorflow/serving:2.7.0

COPY beans-model /models/beans-model/1

ENV MODEL_NAME="beans-model"
```

To build docker images from the above files run the following command:

```bash
docker build -t beans-model-gateway:v02 -f model-gateway.dockerfile .
```

```bash
docker build -t beans-model:xception_final_model -f model-serving.dockerfile .
```

To run docker container from those images run the following command:

```bash
docker run -it --rm \
-p 8500:8500 \
beans-model:xception_final_model
```

```bash
docker run -it --rm \
-p 9696:9696 \
beans-model-gateway:v02
```

To test the service running as expect, run the following command:

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

**NOTE**: switch between `localhost:8500` and `localhost:9696` to separate test the gateway and serving services.
