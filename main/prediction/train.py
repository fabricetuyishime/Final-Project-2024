import os
import cv2
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define paths to your fish image folders
    healthy_fish_path = os.path.join(current_directory, "../../media/dataset/healthy")
    sick_fish_path = os.path.join(current_directory, "../../media/dataset/sick")

    # Load images and labels (sick: 1, healthy: 0)
    images = []
    labels = []

    # Loop through images in both folders
    for path in [sick_fish_path, healthy_fish_path]:
        for img_file in os.listdir(path):
            img = cv2.imread(os.path.join(path, img_file))
            img = cv2.resize(img, (100, 100))  # Resize images to 100x100
            images.append(img.flatten())  # Flatten image to 1D array for features
            labels.append(1 if path == sick_fish_path else 0)  # Assign labels

    # Convert data to numpy arrays
    images = np.array(images)
    labels = np.array(labels)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=42
    )

    # Create and train the SVM model
    svc_model = SVC()
    svc_model.fit(X_train, y_train)

    # Predict on unseen test data
    predictions = svc_model.predict(X_test)

    # Evaluate model performance (accuracy)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {round(accuracy * 100, 2)} %")

    # After training your model (e.g., svc_model)
    with open("model-8.pkl", "wb") as f:
        pickle.dump(svc_model, f)
