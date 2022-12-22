import requests

# url = "http://localhost:9696/predict" # Test model gateway
# url = "http://localhost:8080/predict" # Test model serving
url = ""  # Put URL gateway here

# source images
# https://huggingface.co/datasets/beans/viewer/default/test

# Healthy
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/98/image/image.jpg"

# Bean rust
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/84/image/image.jpg"

# Angular_leaf_spot
# "https://datasets-server.huggingface.co/assets/beans/--/default/test/24/image/image.jpg"

data = {
    "url": "https://datasets-server.huggingface.co/assets/beans/--/default/test/84/image/image.jpg"
}

result = requests.post(url, json=data).json()
print(result)
