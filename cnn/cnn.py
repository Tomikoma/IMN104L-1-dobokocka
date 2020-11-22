import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras import layers
from cnn.preprocess import preprocess
import matplotlib.pyplot as plt
import pathlib


img_height = 256
img_width = 256
batch_size = 32

data_augmentation = tf.keras.Sequential(
    [
        layers.experimental.preprocessing.RandomFlip("horizontal", input_shape=(img_height, img_width, 1)),
        layers.experimental.preprocessing.RandomRotation(0.1),
        layers.experimental.preprocessing.RandomZoom(0.1),
    ]
)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), strides=(1, 1), padding='same', activation='relu'),
    layers.Conv2D(32, (5, 5), strides=(2, 2), padding='same', activation='relu'),
    layers.Conv2D(32, (5, 5), strides=(2, 2), padding='same', activation='relu'),
    layers.Conv2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu'),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(11, activation='softmax')
])


def train_cnn():
    train_ds, val_ds = preprocess()

    class_names = train_ds.class_names
    print(class_names)

    model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    epochs = 10
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size
    )

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    model.save('cnn/model_cnn.h5')
    print("Saved model to disk")

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open("cnn/model_cnn.tflite", "wb").write(tflite_model)

    print("Saved TFLite model to disk")

def predict_cnn(img_path):
    model = models.load_model('cnn/model_cnn.h5')



    img = tf.keras.preprocessing.image.load_img(img_path,color_mode='grayscale',interpolation="nearest", target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    highest= 0
    value = 0
    print(np.argmax(predictions[0])+2)


