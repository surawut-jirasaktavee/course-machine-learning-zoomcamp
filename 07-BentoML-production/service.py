from curses.ascii import US
from tokenize import Number
import bentoml

import numpy as np

from bentoml.io import JSON
from bentoml.io import NumpyNdarray
from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str
    age: int
    country: str
    rating: float


# model1: mlzoomcamp_homework:qtzdz3slg6mwwdu5
# model2: mlzoomcamp_homework:jsi67fslz6txydu5

# model_a_runner = bentoml.sklearn.get("mlzoomcamp_homework:qtzdz3slg6mwwdu5").to_runner()
model_b_runner = bentoml.sklearn.get("mlzoomcamp_homework:jsi67fslz6txydu5").to_runner()
# dv = model_ref.custom_objects['dictVectorizer']

svc = bentoml.Service("credit_risk_classifier", runners=[model_b_runner])

@svc.api(input=NumpyNdarray(shape=(-1, 4), dtype=np.float32, enforce_dtype=True, enforce_shape=True), output=JSON())
async def classify(vector):
   
    # application_data = credit_application.dict()
    
    # vector = dv.transform(application_data)
    prediction = await model_b_runner.predict.async_run(vector)
    
    print(prediction)
    
    result = prediction[0]
    
    if result > 0.5:
        return { "status": "DECLINED"}
    elif result > 0.25:
        return { "status": "MAYBE" }
    else:
        return { "status": "Approved" }
