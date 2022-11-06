# MIDTERM PROJECT

This is the `Midterm` project from [Machine Learning Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp) of [DataTalkClubs](https://datatalks.club)

## PROJECT NAME: Credit risk scoring

## PROBLEM DESCRIPTION

Recently, Banks and credit card companies use our credit scores to evaluate potential risk when the customer want to lending money. But for traditional credit scoring uses a `scores card` method that based on broad segments and will deny credit to consumers without considering their current situation. This traditional methods may also give credit to consumers, called churners that taking out a large number of reward credit cards but are not profitable for the issuers.

The Credit risk scoring from Machine learning method is the great solution for this issue by using more data to provide an individualized credit score based on factors including current income, employment opportunity, recent credit history and ability to earn in addition to older credit history. This approach allows banks and credit card companies the ability to more accurately assess each borrower and allows them to provide credit to people who would have been denied under the scorecard system such as new college graduates or temporary foreign nationals. The Credit risk scoring can also adapt to new problems.

## DATASET

For see the dataset information. Please see the [link](https://www.openml.org/search?type=data&sort=runs&status=active&id=31)

## PROJECT INSTRUCTION

For reproduction this project follow the step below:

First you need to clone this repo

```bash
git clone https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp.git
```

### PROJECT STRUCTURE

- midterm-project
  - dataset
    - ...
  - note
    - ...
  - src
    - ...
  - Pipfile
  - Pipfile.lock
  - README.md

update pip package manager for python package and use pip to install `pipenv` then run pipenv command to install dependencies from this midterm project.

```bash
python -m pip install --upgrade pip
pip install pipenv
pipenv install
```

then activate to the environment

```bash
pipenv shell
```

Navigate to `src` folder. (This folder contain all neccessary things to implement the service)

- src
  - `notebook.ipynb` include:
    - [x] Dataset loaded
    - [x] Data cleaning
    - [x] EDA
    - [x] Data preparation
    - [x] Feature importance analysis
    - [x] Model training
    - [x] Hyper-parameter tuning
    - [x] Model selection
  - `train.py` include:
    - [x] Export training final model in to the script
    - [x] Dataset loader
    - [x] Data cleaning
    - [x] Data preparation
    - [x] Model training
    - [x] Model evaluation
    - [x] Model saving with `BentoML`
  - `predict.py` include:
    - [x] Loading the model
    - [x] Serving the model with web service with `BentoML`
  - bentoml.yaml (BentoML serving)
  - locustfile.py (load test)
  - customer.json (test data) 
  - customer2.json (test data)

In order to serving the model locally run the command:

```bash
bentoml serve --production --reload
```

Then you can go to the `localhost:3000` to test the test data in the `customer.json` and `customer2.json` with the swagger ui.
This model is the batchable model with the feature of `BentoML` 

You can select type of your model in the `saveModel` function in the `train.py`.

```python
train.py

...

def saveModel(model_name: str, enableBatch: None, model, dv):
    
    import bentoml
    
    if enableBatch:
        bentoml.xgboost.save_model(model_name, model,
                                   custom_objects={
                                       'dictVectorizer': dv
                                   },
                                   signatures={
                                       "predict": {
                                           "batchable": True,
                                           "batch_dim": 0
                                       }
                                   })
    else:
        bentoml.xgboost.save_model(model_name, model,
                               custom_objects={
                                   'dictVectorizer': dv
                               })
    
    logging.info('Saved model')
    
    print("Save model successfully...")
    
...
```

To inspect the saved model from training session. you can check with the command:

```bash
bentoml models list
```

you will see the tag that `BentoML` generate with your model name. you can use `<model_name>:<latest>` to refer to your latest model.
this will use to load the model to serving the service.

![bentoml_model_list](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/bentoml_model_list.png)

### SWAGG UI

![swagger_ui](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/swagger_ui.png)
![swagger_ui](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/swagger_ui2.png)

Copy the `customer.json` and paste into swagger ui and execute to check the result.

![test_data](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/test_data.png)
![get_result](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/get_result.png)

### LOCUST UI

In order to you want to test the number of request that your service can handle. go to `localhost:8089` and setting up you number from the ui.

![locust_ui](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/locust_ui.png)

Now, Let's deploy this model to the cloud provider to give the ability and performance more locally. I will use AWS provider in this project.

To deploying the model with container service (`AWS fargate`). I will build the image of the model service and then push to the registry (`AWS ECR`). this way I can get the model from the registry and use the image to deploy as the task in the fargate cluster. you will need `AWS CLI` to use aws commandline to login and push your image.

### AWS ELASTIC CONTAINER REGISTRY

Let's build the image first. For this task i will use `BentoML` to build the image. Create the `bentofile.yaml` and put the necessary thing for your service.

```yaml
service: "predict.py:svc"
labels:
  owner: credit_risk-team
  project: credit_risk_scoring
include:
- "predict.py"
python:
  packages:
    - xgboost
    - sklearn
    - pydantic
```

Then run the command:

```bash
bentoml build
```

![bentoml_build](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/bentoml_build.png)

After build finish the tag of your image will appear as above. run the next command with that tag.

```bash
bentoml containerize <model_name>:<tag> --platform=linux/amd64
```

I have specify the base platform that I will build with the image by put `--platform=linux/amd64` to the command.

![bentoml_containerize](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/bentoml_containerize_build.png)

After build finish. Check image that you just build

```bash
docker images
```

Now let's push the image the to `AWS ECR`. Login to the `AWS ECR` and tag the image and then push it.
To create `AWS Elastic Container Registry` see this [link](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/note/ECR.md) and follow the steps. 

After finish those steps you will see your image in the reposity as below:

![push_image](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/push_image.png)

### AWS ELASTIC CONTAINER SERVICE (FARGATE CLUSTER)

In order to serve the model with `AWS FARGATE CLUSTER` follow the steps from this [link](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/note/ECS.md)

![fargate_cluster_running](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_running.png)

After deploy the model to the `AWS FARGATE CLUSTER`. Now the model ready to serve the `Credit risk classify` for every customer data.

- Go to the Cluster on the left bar.
- Select the task that you created.
- In the task info you will see the publicIP address
- Open the browser with the `publicIP:port`

![task_info](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/fargate_task_info.png)

![credit_risk_classifier_service](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/credit_risk_classifier_service.png)

### CREDIT RISK CLASSIFIER DEMO

[##TODO] 

ADD SERVICE DEMO HERE
