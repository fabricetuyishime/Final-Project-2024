import cv2
import pickle
import numpy as np


def load_fish_model(model_path):
    if model_path.endswith(".pkl"):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    else:
        raise ValueError("Unsupported model format. Please specify correct path.")


def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (100, 100))
    return img.flatten()


def identify_image(new_image_path):
    model = load_fish_model("main/prediction/model-8.pkl")
    new_image = preprocess_image(new_image_path)

    prediction = model.predict(np.array([new_image]))[0]

    if prediction > 0.5:
        return "Predicted: Sick Fish"
    else:
        return "Predicted: Healthy Fish"
