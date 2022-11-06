from locust import task, between, HttpUser
from locust.exception import RescheduleTask

from json import JSONDecodeError

sample = {
    "checking_status": "0<=X<200",
    "duration": 48.0,
    "credit_history": "existing_paid",
    "purpose": "new_car",
    "credit_amount": 35000.0,
    "savings_status": "<100",
    "employment": "7<=X<10",
    "installment_commitment": 10.0,
    "personal_status": "div/dep/mar",
    "sex": "male",
    "other_parties": "yes",
    "residence_since": 5.0,
    "property_magnitude": "life_insurance",
    "age": 46.0,
    "other_payment_plans": "yes",
    "housing": "own",
    "existing_credits": 3.0,
    "job": "skilled",
    "num_dependents": 1.0,
    "own_telephone": "yes",
    "foreign_worker": "yes"
}

class CreditRiskUser(HttpUser):
    """
    Usage:
        Start locust load testing client with:
            locust -H http://localhost:3000
        Open browser at http://0.0.0.0:8089, adjust desired number of users and spawn
        rate for the load test from the Web UI and start swarming.
    """

    @task    
    def predictClassify(self):
       
        try:
            response = self.client.get("/predictClassify", catch_response=True)
            if response.text != "Success":
                response.failure("Got wrong response")
            elif response.status_code == 404:
                raise RescheduleTask()
        except JSONDecodeError:
            response.failure("Response could not be decoded as JSON")
        except:
            self.client.post("/predictClassify", json=sample)

    wait_time = between(0.01, 2)
