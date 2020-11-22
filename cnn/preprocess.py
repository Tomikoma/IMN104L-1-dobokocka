import pathlib
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import preprocessing


def preprocess():
    data_dir = pathlib.Path("images")

    batch_size = 32
    img_height = 256
    img_width = 256



    train_ds = preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='int',
        color_mode='grayscale',
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='int',
        color_mode='grayscale',
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    return train_ds, val_ds