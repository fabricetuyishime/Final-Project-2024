import pickle
import cv2
from sklearn.svm import SVC  # Assuming you used scikit-learn for training
import numpy as np

# Import pickle if you saved the model with pickle


# Define function to load the model (replace 'SVC' with your model class if different)
def load_fish_model(model_path):
    if model_path.endswith(".pkl"):  # Check for pickle extension
        with open(model_path, "rb") as f:
            return pickle.load(f)  # Load model using pickle
    # Add elif blocks here for other model saving formats (e.g., TensorFlow/PyTorch)
    else:
        raise ValueError("Unsupported model format. Please specify correct path.")


# Define function to preprocess an image (modify based on your preprocessing steps)
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (100, 100))  # Assuming you resized images during training
    return img.flatten()  # Flatten image to 1D array for features


# Load the trained model (replace 'model.pkl' with your path)
model = load_fish_model("model-8.pkl")

# Get the path to your new fish image
new_image_path = "./healthy-fish.jpeg"  # Replace with your image path

# Preprocess the new image
new_image = preprocess_image(new_image_path)

# Make prediction using the loaded model
prediction = model.predict(np.array([new_image]))[
    0
]  # Assuming model predicts probability

# Print the prediction (modify based on your labels)
if prediction > 0.5:
    print(f"Predicted: {round(prediction * 100, 2)} % Sick Fish")
else:
    print(f"Predicted: {round((1 - prediction) * 100, 2)} % Healthy Fish")

# You can adjust the threshold (0.5) for probability based on your model's output
