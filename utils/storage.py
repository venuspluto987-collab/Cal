import pickle
import os

MODEL_PATH = "saved_models"


def save_model(model_name, obj):

    os.makedirs(MODEL_PATH, exist_ok=True)

    filepath = f"{MODEL_PATH}/{model_name}.pkl"

    with open(filepath, "wb") as f:
        pickle.dump(obj, f)


def load_model(model_name):

    filepath = f"{MODEL_PATH}/{model_name}.pkl"

    with open(filepath, "rb") as f:
        return pickle.load(f)


def get_models():

    os.makedirs(MODEL_PATH, exist_ok=True)

    return [
        file.replace(".pkl", "")
        for file in os.listdir(MODEL_PATH)
        if file.endswith(".pkl")
    ]
