import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from fbs_runtime.application_context.PyQt5 import ApplicationContext




def predict_cnn(img_path):
    model = models.load_model(ApplicationContext().get_resource("model_cnn_2.h5"))



    img = tf.keras.preprocessing.image.load_img(img_path,color_mode='grayscale',interpolation="nearest", target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    highest= 0
    value = 0
    return np.argmax(predictions[0])+2
