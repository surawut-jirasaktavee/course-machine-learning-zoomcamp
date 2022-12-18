import tensorflow as tf
from tensorflow import keras
print(f"Tensorflow version: {tf.__version__}")
import tensorflow_datasets as tfds

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


# Configurations class
class CONFIG:
    
    img_size = 299
    seed = 42
    AUTOTUNE = tf.data.AUTOTUNE
    learning_rate = 0.01
    size_inner = 10
    droprate = 0.0
    batch_size = 32
    epochs = 30
    num_classes = 3
    workdir = "workdir"
    

class DATASET():
    
    def __init__(self, dataset_name: str='beans'):
        self.dataset_name = dataset_name
    
    
    def _check_instance(self, ds):
        assert isinstance(ds, tf.data.Dataset)
        print(ds)
    
    
    def download_dataset(self, dataset_name: str='beans'):
        
        (train_ds, val_ds, test_ds), metadata = tfds.load(
            self.dataset_name, 
            split=["train[:80%]", "train[80%:90%]", "train[90%:]"],
            with_info=True, 
            as_supervised=True,
            data_dir="../dataset",
        )
        self._check_instance(train_ds)
        self._check_instance(val_ds)
        self._check_instance(test_ds)
        
        return (train_ds, val_ds, test_ds), metadata
   
   
    def get_num_class(self):
        
        num_classes = self.metadata.features["label"].num_classes
        print(f"This beans dataset has : {num_classes} classes")
        
        return num_classes


def resize_and_rescale(img_size):
    
    img = keras.Sequential([
        keras.layers.Resizing(img_size, img_size),
        keras.layers.Rescaling(1.0 / 255)
    ])
    
    return img


def prepare_ds(ds, 
               num_parallel_calls=CONFIG.AUTOTUNE,
               seed=CONFIG.seed, 
               batch_size=CONFIG.batch_size,
               shuffle=False):
    
    ds = ds.map(lambda x: y (resize_and_rescale(x), y),
                num_parallel_calls=num_parallel_calls)
    
    if shuffle:
        ds = ds.shuffle(seed)
        
    ds = ds.batch(batch_size)
    
    return ds.prefetch(buffer_size=num_parallel_calls)


def augmentation(seed=CONFIG.seed):
    
    img = keras.Sequential(
        [
            keras.layers.RandomFlip("horizontal"),
            keras.layers.RandomRotation(0.1),
            keras.layers.RandomCrop(150, 150), seed=seed
        ]
    )
    
    return img

def generate_final_xception_basd_model_aug(include_top=False,
                                           img_size=CONFIG.img_size,
                                           trainable=False, 
                                           learning_rate=CONFIG.learning_rate, 
                                           size_inner=CONFIG.size_inner, 
                                           droprate=CONFIG.droprate):

    base_model = Xception(
        weights="imagenet",
        include_top=include_top,
        input_shape=(img_size, img_size, 3),
    )

    base_model.trainable = trainable

    
    #########################################

    inputs = keras.Input(shape=(img_size, img_size, 3))
    x = augmentation(inputs)
    base = base_model(x, training=False)
    vectors = keras.layers.GlobalAveragePooling2D()(base)
    inner = keras.layers.Dense(size_inner, activation="relu")(vectors)
    drop = keras.layers.Dropout(droprate)(inner)
    outputs = keras.layers.Dense(config.num_classes)(drop)
    model = keras.Model(inputs, outputs)

    #########################################

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])

    return model


def checkpoint_setup(file_name="xception_v1-{epoch:02d}-{val_loss:.2f}.h5"):
    version = file_name[:11]
    checkpoint_filepath = os.path.join(config.workdir, version, "ckpt", file_name)
    checkpoint = keras.callbacks.ModelCheckpoint(
        checkpoint_filepath, save_best_only=True, monitor="val_accuracy", mode="max"
    )
    return checkpoint


def visualize_result(history, epochs):
    
    plt.plot(history.history["accuracy"], label="train")
    plt.plot(history.history["val_accuracy"], label="val")
    plt.xticks(np.arange(epochs))
    plt.legend()

    
def model_evaluation(model, test_ds):
    model.evaluate(test_ds)
    

def save_model(model, model_name='model.h5', format='h5'):
    from pathlib import Path
    
    model_path = Path("./models")
    model_path.mkdir(parents=True, exist_ok=True)
    
    model.save(f'{model_path}/{model_name}', save_format=format)
    print("Save model successfully")


def main(model_name_to_save='model.h5'):
    
    config = CONFIG()
    
    dataset = DATASET()
    (train_ds, val_ds, test_ds), metadata = dataset.download_dataset('beans')
    
    file_name = "xception_v1-epoch_{epoch:02d}-val_loss_{val_loss:.2f}.h5"
    checkpoint = checkpoint_setup(file_name)
    
    train_ds = prepare_ds(train_ds, shuffle=True)
    val_ds = prepare_ds(val_ds)
    test_ds = prepare_ds(test_ds)
     
    # Use default arguments
    model = generate_final_xception_basd_model_aug()
    model.summary()
    history = model.fit(
        train_ds, validation_data=val_ds,
        epochs=config.epochs,
        callbacks=[checkpoint]
        )
   
    visualize_result(history, seed=config.seed)
    
    model_evaluation(model, test_ds)
    
    save_model(model_name_to_save)
    
    
if __name__ == "__main__":
    
    model_name = "beans_model.h5"
    main(model_name)