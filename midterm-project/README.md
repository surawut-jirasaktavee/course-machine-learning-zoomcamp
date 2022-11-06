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
This model is the batchable model with the feature of `BentoML` you can select type of your model in the `saveModel` function in the `train.py`.

### SWAGG UI

![swagger_ui](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/swagger_ui.png)
![swagger_ui](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/swagger_ui2.png)

Copy the `customer.json` and paste into swagger ui and execute to check the result.

![test_data](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/test_data.png)
![get_result](https://github.com/surawut-jirasaktavee/course-machine-learning-zoomcamp/blob/main/midterm-project/images/get_result.png)

