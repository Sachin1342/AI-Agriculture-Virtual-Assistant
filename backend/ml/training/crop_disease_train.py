"""Crop disease image classifier training script (local-laptop friendly).

Steps:
- Load dataset (directory if available, otherwise synthetic fallback)
- Preprocess (resize + MobileNetV2 preprocess)
- Train (transfer learning with frozen base + tiny fine-tune)
- Evaluate (loss, accuracy)
- Save model
- Print metrics
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "disease_model.keras"
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16


def _dataset_candidates() -> list[Path]:
    root = BASE_DIR.parents[1]
    return [
        root / "plant_disease_dataset",
        root / "data" / "plant_disease_dataset",
        root / "plant diseases" / "New Plant Diseases Dataset(Augmented)" / "New Plant Diseases Dataset(Augmented)" / "train",
    ]


def _build_synthetic(tf):
    x = tf.random.uniform((120, 224, 224, 3), 0, 255)
    y = tf.random.uniform((120,), minval=0, maxval=8, dtype=tf.int32)
    ds = tf.data.Dataset.from_tensor_slices((x, y)).shuffle(120).batch(BATCH_SIZE)
    train = ds.take(6)
    val = ds.skip(6).take(2)
    return train, val, 8


def _load_dataset(tf):
    for path in _dataset_candidates():
        if path.exists() and path.is_dir():
            print(f"Loading image dataset from: {path}")
            train_ds = tf.keras.utils.image_dataset_from_directory(
                path,
                validation_split=0.2,
                subset="training",
                seed=42,
                image_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
            )
            val_ds = tf.keras.utils.image_dataset_from_directory(
                path,
                validation_split=0.2,
                subset="validation",
                seed=42,
                image_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
            )
            num_classes = len(train_ds.class_names)
            return train_ds, val_ds, num_classes

    print("No image directory found, using synthetic image dataset for smoke training.")
    return _build_synthetic(tf)


def main() -> None:
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise SystemExit("TensorFlow not installed. Install backend requirements first.") from exc

    train_ds, val_ds, num_classes = _load_dataset(tf)

    autotune = tf.data.AUTOTUNE
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.1),
        ]
    )

    train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=autotune).prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)

    base = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
    base.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
    ]

    history_head = model.fit(train_ds, validation_data=val_ds, epochs=8, callbacks=callbacks, verbose=1)

    # tiny fine-tune for better local quality without heavy cost
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    history_ft = model.fit(train_ds, validation_data=val_ds, epochs=4, callbacks=callbacks, verbose=1)

    loss, acc = model.evaluate(val_ds, verbose=0)
    model.save(MODEL_PATH)

    best_val_acc = float(np.max(history_head.history.get("val_accuracy", [0.0]) + history_ft.history.get("val_accuracy", [0.0])))

    print("\n=== Crop Disease Training Metrics ===")
    print(f"Classes: {num_classes}")
    print(f"Validation Loss    : {loss:.4f}")
    print(f"Validation Accuracy: {acc:.4f}")
    print(f"Best Val Accuracy  : {best_val_acc:.4f}")
    print(f"Saved model: {MODEL_PATH}")


if __name__ == "__main__":
    main()
