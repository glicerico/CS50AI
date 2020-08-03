import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    ## REMOVE!!
    # check_predictions(model, x_test, y_test)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def check_predictions(model, x_test, y_test):
    prob_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    preds = prob_model.predict(x_test)
    plot_predictions(preds, x_test, y_test)


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(predicted_label,
                                         100 * np.max(predictions_array),
                                         true_label),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(NUM_CATEGORIES))
    plt.yticks([])
    thisplot = plt.bar(range(NUM_CATEGORIES), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


def plot_predictions(predictions, test_images, test_labels):
    # Plot the first X test images, their predicted labels, and the true labels.
    # Color correct predictions in blue and incorrect predictions in red.
    num_rows = 5
    num_cols = 3
    num_images = num_rows * num_cols
    plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
        plot_image(i, predictions[i], test_labels, test_images)
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
        plot_value_array(i, predictions[i], test_labels)
    plt.tight_layout()
    plt.show()


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    labels = []
    images = []
    cwd = os.getcwd()
    for directory in os.listdir(data_dir):
        dir_path = os.path.join(cwd, data_dir, directory)
        if os.path.isdir(dir_path):  # Only look inside directories
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                src = cv2.imread(file_path)  # read image
                img = cv2.resize(src, (IMG_WIDTH, IMG_HEIGHT))  # Resize image
                # Append label and image to lists
                labels.append(int(directory))
                images.append(img)
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    num_conv = 3
    num_filters = [16, 16, 16]
    filter_dims = [(5, 5), (4, 4), (3, 3)]
    dropout_rate = 0.10
    num_pooling = 1
    pool_dims = [(2, 2)]
    num_hidden = 1
    hidden_dims = [128, 128]

    model = tf.keras.models.Sequential()

    # Add convolutional layers with num_filters using the specified-size kernel
    for i in range(num_conv):
        model.add(tf.keras.layers.Conv2D(
            num_filters[i], (filter_dims[i][0], filter_dims[i][1]), activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ))

    for i in range(num_pooling):
        # Add max-pooling layers, using custom pool sizes
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(pool_dims[i][0], pool_dims[i][1])))

    # Flatten units
    model.add(tf.keras.layers.Flatten())

    # Add hidden layers with dropout
    for i in range(num_hidden):
        model.add(tf.keras.layers.Dense(hidden_dims[i], activation="relu"))
        model.add(tf.keras.layers.Dropout(dropout_rate))

    # Add an output layer with output units for all sign categories
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES))

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
