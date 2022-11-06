import bentoml
from bentoml.io import JSON

from pydantic import BaseModel

class CustomerCreditApplication(BaseModel):
    """
    Args:
        BaseModel (Any): Get metadata_dict from BaseModel input 
        (Please put the desire customer application data type.)
    """
    checking_status: str
    duration: float
    credit_history: str
    purpose: str
    credit_amount: float
    savings_status: str
    employment: str
    installment_commitment: float
    personal_status: str
    sex: str
    other_parties: str
    residence_since: float
    property_magnitude: str
    age: float
    other_payment_plans: str
    housing: str
    existing_credits: float
    job: str
    num_dependents: float
    own_telephone: str
    foreign_worker: str

model_tag = 'credit_risk_model:latest'
model_ref = bentoml.xgboost.get(model_tag)
model_runner = model_ref.to_runner() 
dv = model_ref.custom_objects['dictVectorizer']

svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])

@svc.api(input=JSON(pydantic_model=CustomerCreditApplication), output=JSON())
async def predictClassify(customer_credit_application):
    """
    Args:
        customer_credit_application (Class Inheritance): transform customer credit application into a dictionary

    Returns:
        List[float]: get result > 0.0 and translate customer credit application to human actions and return a result
    """    
    application_data = customer_credit_application.dict()
    dict_vector = dv.transform(application_data)
    prediction = await model_runner.predict.async_run(dict_vector)
    
    result = prediction[0]
    
    print(f"[PREDICTION RESULT]: Credit risk score for this customer is: {result}")
    
    if result < 0.5:
        return { "status": "DECLINED" }
    elif 0.60 > result > 0.50:
        return { "status": "APPROVED 50%" }
    elif 0.70 > result > 0.60:
        return { "status": "APPROVED 60%" }
    elif 0.80 > result > 0.70:
        return { "status": "APPROVED 70%" }
    elif 0.90 > result > 0.80:
        return { "status": "APPROVED 80%" }
    else:
        return { "status": "APPROVED 100%"}
