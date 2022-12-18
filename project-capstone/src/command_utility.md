# Command line utility

## Run Docker image with Tensorflow Serving

```bash
docker run -it --rm \
    -p 8500:8500 \
    -v "$(pwd)/beans-model:/model/beans-model/1" \
    -e MODEL_NAME="beans-model" \
    tensorflow/serving:2.7.0
```

## Convert tf-serving.ipynb to scrtip

```bash
!jupyter nbconvert --to script tf-serving.ipynb
```

## Build docker image that by model_serving.dockerfile
```bash
docker build -t beans-model:xception_final_model -f model_serving.dockerfile .
```


## Run docker image that build from model_serving.dockerfile
```bash
docker run -it --rm \
-p 8500:8500 \
beans-model:xception_final_model
```

## Build docker image that by model_gateway.dockerfile
```bash
docker build -t beans-model-gateway:v01 -f model_gateway.dockerfile .
```

## Run docker image that build from model_gateway.dockerfile

```bash
docker run -it --rm \
-p 9696:9696 \
beans-model-gateway:v01
```