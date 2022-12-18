import numpy as np

import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from keras_image_helper import create_preprocessor
from proto import np_to_protobuf

from flask import Flask, request, jsonify


def preprocessor( url: str, base_model: str='xception', target_size: int=299):
    
    import os 
    host = os.getenv("TF_SERVING_HOST", "localhost:8500")
    channel = grpc.insecure_channel(host)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    preprocessor = create_preprocessor(base_model, target_size=(target_size, target_size))
    X = preprocessor.from_url(url)
    return X, stub


def prepare_request(X, 
                    model_name: str='beans-model',
                    signature_name: str='serving_default',
                    input: str='input_26'):
    
    pb_request = predict_pb2.PredictRequest()
    pb_request.model_spec.name = model_name
    pb_request.model_spec.signature_name = signature_name

    pb_request.inputs[input].CopyFrom(np_to_protobuf(X))

    return pb_request
    
   
def predict(url: str, timeout: float=20.0):

    X, stub = preprocessor(url)
    pb_request = prepare_request(X)
    pb_response = stub.Predict(pb_request, timeout=timeout)
    response = prepare_response(pb_response)
    return response


def prepare_response(pb_response, output: str='dense_19',):
    
    classes = [
    "angular_leaf_spot",
    "bean_rust",
    "healthy"
    ]
    preds = pb_response.outputs[output].float_val
    dict_preds = dict(zip(classes, np.abs(preds)))
    key_list = list(dict_preds.keys())
    val_list = list(dict_preds.values())
  
    index = val_list.index(min(val_list))
    result = key_list[index]
   
    return  result


app = Flask("tf_serving_gateway")

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)


if __name__ == "__main__":

    # url = "https://datasets-server.huggingface.co/assets/beans/--/default/test/9/image/image.jpg"
    # response = predict(url)
    # print(response)
    app.run(debug=True, host="0.0.0.0", port=9696)
