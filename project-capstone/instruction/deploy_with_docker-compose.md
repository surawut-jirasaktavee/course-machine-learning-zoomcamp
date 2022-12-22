# Deploy Tensorflow serving model with Docker image

To deploy Tensorflow serving model with docker-compose, follow the following instructions and use `docker-compose.yaml` file to deploy Tensorflow serving model.

```docker-compose
version: "3.9"
services:
  beans-model:
    image: beans-model:xception_final_model
  beans-model-gateway:
    image: beans-model-gateway:v02
    environment:
      - TF_SERVING_HOST=beans-model:8500
    ports:
      - "9696:9696"
```

**NOTE**: Need to create two docker images in order to use the this docker-compose.

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
