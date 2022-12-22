# MACHINE LEARNING ZOOMCAMP

This is the `Project Capstone cohort-1` for [Machine Learning Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp) of [DataTalkClubs](https://datatalks.club/)

## PROJECT NAME: Bean Serving Classification

## PROBLEM DESCRIPTION

The purpose of this project is to show what I have learned about the machine learning zoomcamp course and how I understand all of it. And once I have understood what I can apply for it. With this purpose I have decided to apply with my interest or favorite things that is `Bean` I always love to eat beans. And I will always eat beans everyday. So I have combined my knowledge from this course and apply to my interest/favorite and show what I can do with it. 

This project is `Computer Vision` project that try to classify the classes of objects from the images(bean images).

## DATASET

To see the dataset information. Please see the [docs](https://www.tensorflow.org/datasets/catalog/beans).

Dataset Github: https://github.com/AI-Lab-Makerere/ibean/

Explore Dataset: https://knowyourdata-tfds.withgoogle.com/#tab=STATS&dataset=beans

## PROJECT INSTRUCTIONS

This project can reproduction with different ways as follows:

1. Docker images
2. Docker compose
3. Kubernetes local cluster with Kind or Docker desktop
4. AWS Elastic Kubernetes Service

First clone this repository into your project directory

```bash
git clone https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp.git
```

Navigate to the `project-capstone` folder

```bash
tree
```

If `tree` had installed already the hierarchy of the project will show up.

### PROJECT DEPENDENCIES

For experiment parts will be inside the notebook folder. Install the dependencies for experiment parts

Inside of `project-capstone` folder run the following command:

```bash
pipenv install --system --deploy
pipenv shell
```

### EXPERIMENT AND TRAINING

Now the notebook can run as normal as it should be.

I have separate notebook to 3 parts:

1. `notebook.ipynb` for experiment purposes
2. `save_model.ipynb` for model converting and saving purposes
3. `tf_serving.ipynb` for test model serving purposes

After the experiment has finished the notebook should convert to the Python script that can be used to run the experiment parts easily.

To convert the notebook to the Python script run the following command:

```bash
jupyter nbconvert --to script <your notebook name>
```

After experimentation I

To save the model after final training session, use the following command:

```bash
saved_model_cli show --air <model_name_folder> --all
```

Save the model at S3 bucket.

```bash
aws s3 cp <soumodel_name_folderrce> S3_bucket> --recursive
```

### DEPLOYMENT

To deploy model with `Dockerfile` follow with the [instruction](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/instruction/deploy_with_dockerfile.md)

To deploy model with `docker-compose` follow with the [instruction](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/tree/main/project-capstone/instruction#:~:text=deploy_with_docker%2Dcompose.md)

To deploy model with `kubernetes-local-cluster` follow with the [instruction](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/instruction/deploy_with_kubernetes-local.md)

To deploy model with `kubernetes with AWS EKS` follow with the [instruction](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/project-capstone/instruction/deploy_with_kubernetes-eks.md)

### Additional deploy Tensorflow serving with `Streamlit` app with Steamlit Cloud

I have created folder app to create steamlit application and docker image to run `Streamlit app` inside docker container to use Tensorflow serving. This will deploy the local application and not publish to the public.

In case to publish this application to the internet you will have to create new `Github` repository and store this folder inside this repository and follow the steps from `Streamlit`. To deploy the application with Steamlit Cloud see the [link](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

my application on github repo: https://github.com/surawut-jirasaktavee/tf-serving-app

## BEAN CLASSICATION APP DEMO

https://www.youtube.com/watch?v=cM6nmXbMWGI

## ABOUT PROJECT

This project includes:

[x] Problem description
[x] Dataset downloading
[x] EDA
[x] Data preparation
[x] Data augmentation
[x] Model training
[x] Model selection
[x] Model hyper parameter tuning
[x] Model evaluation
[x] Exporting notebook to script (final train model)
[x] Model deployment
[x] Reproducibility
[x] Dependency and environment management
[x] Containerization
[x] Cloud deployment

This project excludes:

[] Unit tests
[] Integration tests

## PROJECT STACK

- Python
- Tersorflow and Keras
- AWS ECR
- AWS S3
- AWS EKS (Kubernetes)
- AWS EC2
- Jupyter notebook
- Pipenv
- Docker
- etc

## IN CASE TO ASK SOME QUESTION ABOUT THE PROJECT

Slack: U042PQU7P4Y

LINKEDIN: https://www.linkedin.com/in/surawut-jirasaktavee/

# THANK YOU 🙏
