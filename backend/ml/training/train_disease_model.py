from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "disease_model.keras"


def build_model(num_classes: int = 10):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def train() -> None:
    # Placeholder dataset to keep script runnable in all environments
    x = tf.random.uniform((100, 224, 224, 3), 0, 255)
    y = tf.random.uniform((100,), minval=0, maxval=10, dtype=tf.int32)

    model = build_model(10)
    model.fit(x, y, validation_split=0.2, epochs=2, batch_size=8, verbose=1)
    model.save(MODEL_PATH)
    print(f"Saved disease model to {MODEL_PATH}")


if __name__ == "__main__":
    train()
