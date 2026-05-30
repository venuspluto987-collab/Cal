import os
import pickle
import json

MODEL_PATH = "saved_models"
WIDGET_PATH = "saved_widgets"
STORY_PATH = "saved_stories"
PLANNING_PATH = "saved_planning"


# ==========================
# MODEL
# ==========================

def save_model(name, obj):

    os.makedirs(MODEL_PATH, exist_ok=True)

    with open(
        f"{MODEL_PATH}/{name}.pkl",
        "wb"
    ) as f:

        pickle.dump(obj, f)


def load_model(name):

    with open(
        f"{MODEL_PATH}/{name}.pkl",
        "rb"
    ) as f:

        return pickle.load(f)


def get_models():

    os.makedirs(MODEL_PATH, exist_ok=True)

    return [

        file.replace(".pkl", "")

        for file in os.listdir(MODEL_PATH)

        if file.endswith(".pkl")
    ]


# ==========================
# WIDGETS
# ==========================

def save_widget(name, obj):

    os.makedirs(WIDGET_PATH, exist_ok=True)

    with open(
        f"{WIDGET_PATH}/{name}.json",
        "w"
    ) as f:

        json.dump(
            obj,
            f,
            default=str
        )


def get_widgets():

    os.makedirs(WIDGET_PATH, exist_ok=True)

    return [

        file.replace(".json", "")

        for file in os.listdir(WIDGET_PATH)

        if file.endswith(".json")
    ]


# ==========================
# STORIES
# ==========================

def save_story(name, obj):

    os.makedirs(STORY_PATH, exist_ok=True)

    with open(
        f"{STORY_PATH}/{name}.json",
        "w"
    ) as f:

        json.dump(
            obj,
            f,
            default=str
        )


def get_stories():

    os.makedirs(STORY_PATH, exist_ok=True)

    return [

        file.replace(".json", "")

        for file in os.listdir(STORY_PATH)

        if file.endswith(".json")
    ]


# ==========================
# PLANNING
# ==========================

def save_planning(name, obj):

    os.makedirs(PLANNING_PATH, exist_ok=True)

    with open(
        f"{PLANNING_PATH}/{name}.json",
        "w"
    ) as f:

        json.dump(
            obj,
            f,
            default=str
        )


def get_planning():

    os.makedirs(PLANNING_PATH, exist_ok=True)

    return [

        file.replace(".json", "")

        for file in os.listdir(PLANNING_PATH)

        if file.endswith(".json")
    ]
