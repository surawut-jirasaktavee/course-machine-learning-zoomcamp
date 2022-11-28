import tflite_runtime.interpreter as tflite
from io import BytesIO
from urllib import request
from PIL import Image
import numpy as np


def download_image(url) -> Image:
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size) -> Image:
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_input(x):
    x /= 255
    return x


def predict(url, img_size):
    """
    Predictions for the given input
    """
    img = download_image(url)
    img = prepare_image(img, img_size)

    x = np.array(img, dtype=np.float32)
    x = np.array([x])
    X = preprocess_input(x)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_index)

    float_preds = pred[0].tolist()

    return float_preds


def lambda_handler(event):  # , context):
    url = event["url"]

    result = predict(url, img_size)

    return result


interpreter = tflite.Interpreter(model_path="dino_dragon_10_0.899.tflife")
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
img_size = (150, 150)

output = lambda_handler(
    "https://upload.wikimedia.org/wikipedia/en/e/e9/GodzillaEncounterModel.jpg"
)
print(output)
