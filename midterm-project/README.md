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
  - notebook.ipynb
  - train.py
  - predict.py
  - bentoml.yaml
  - locustfile.py
  - customer.json
  - customer2.json

I kept all EDA, training, hyper-parameter tuning and model selection processes in `notebook.ipynb`.
