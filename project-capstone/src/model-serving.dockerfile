FROM tensorflow/serving:2.7.0

COPY beans-model /models/beans-model/1

ENV MODEL_NAME="beans-model"

