import json
import datetime

import numpy as np
import keras

DATA_DIR = "../data/"

def load_data(filename):
    # Load the training data
    with open(f"{DATA_DIR}{filename}", "r") as training_data_file:
        training_data = json.load(training_data_file)
    X = np.array(training_data["mfcc"])
    y = np.array(training_data["labels"])
    mapping = np.array(training_data["mapping"])
    return X, y, mapping

def train_model():
    X_train, y_train, mapping = load_data("extracted_mfccs_custom_train.json")
    X_test, y_test, mapping = load_data("extracted_mfccs_custom_test.json")
    X_validation, y_validation, mapping = load_data("extracted_mfccs_custom_validation.json")

    input_shape = (X_train.shape[1], X_train.shape[2])

    # Create model
    model = keras.Sequential()

    # 2 LSTM layers
    model.add(keras.layers.LSTM(units=64,
                                input_shape=input_shape,
                                return_sequences=True))
    model.add(keras.layers.LSTM(units=64))

    # Dense layer
    model.add(keras.layers.Dense(units=64,
                                activation="relu"))
    model.add(keras.layers.Dropout(rate=0.3))

    # Output layer
    model.add(keras.layers.Dense(10, activation="softmax"))

    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer,
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"])
    # Train the CNN
    model.fit(X_train, y_train, validation_data=(X_validation, y_validation), batch_size=32, epochs=30)

    # Evaluate the CNN on the test set
    test_error, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"Accuracy on test set is: {test_accuracy}")

    # Make predictions on a sample
    X = X_test[100]
    y = y_test[100]
    
    X = X[np.newaxis, ...]

    # prediction = [ [0.1, 0.2, ...] ]
    prediction = model.predict(X) # X -> (1, 130, 13, 1)

    # Extract index with max value
    predicted_index = np.argmax(prediction, axis=1) # [3]
    print(f"Expected mapping: {mapping[y]}, Predicted mapping: {mapping[predicted_index]}")

    
    model.save(f"{DATA_DIR}model_{datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.h5")

if __name__ == "__main__":
    train_model()
