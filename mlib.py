"""MLOps Library"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import logging

logging.basicConfig(level=logging.INFO)


def load_model(model="model.joblib"):
    """Grabs model from disk"""

    clf = joblib.load(model)
    return clf


def data():
    df = pd.read_json("webscrapi_fifa_players/data_fifa_players.json")
    return df


def change_data_types(df):
    """change data types for better manage"""

    # cm
    df["height"] = df["height"].str.extract("(\d+)").astype(int)
    # kg
    df["weight"] = df["weight"].str.extract("(\d+)").astype(int)
    # euros
    df["Value"] = pd.to_numeric(df["Value"].str.replace("€|\.", "", regex=True))
    df["Wage"] = pd.to_numeric(df["Wage"].str.replace("€|\.", "", regex=True))

    return df


def get_position_zone(df):
    position_zone = []
    for x in df["preferred_positions"]:

        listb = {"DEFENDING": 0, "MIDFIELD": 0, "ATTACKING": 0, "GOALKEEPER": 0}
        for y in x:
            # print(y)
            if y in ["GK"]:
                listb["GOALKEEPER"] = 1
            else:
                if y in ["LF", "RF", "CF", "ST"]:
                    listb["ATTACKING"] = listb["ATTACKING"] + 1
                if y in ["CAM", "RM", "RW", "CDM", "CM", "LM", "LW"]:
                    listb["MIDFIELD"] = listb["MIDFIELD"] + 1
                if y in ["LB", "LWB", "RB", "RWB", "CB"]:
                    listb["DEFENDING"] = listb["DEFENDING"] + 1

        position_zone.append(max(listb, key=listb.get))

    df.loc[:, "position_zone"] = position_zone
    df = df.drop(columns=["preferred_positions"])

    return df


def one_hot_coding(df):
    """Conver columns type 'object' to one hot coding, then
    delete leaving only the One hot coding"""
    dummies_object = None
    columns_type_object = []

    for i, column_type in enumerate([str(d) for d in df.dtypes]):
        if column_type == "object":
            column_name = df.columns[i]
            columns_type_object.append(column_name)

            dummies = pd.get_dummies(df[column_name], prefix=column_name)

            if dummies_object is None:
                dummies_object = dummies
            else:
                dummies_object = pd.concat([dummies_object, dummies], axis=1)

    df = df.drop(columns_type_object, axis="columns")
    df = pd.concat([df, dummies_object], axis=1)
    return df


def clean_data():
    df = data()
    df = df.drop(columns=["url"])
    df = df.dropna().copy()
    df = change_data_types(df)
    df = get_position_zone(df)
    df = df.drop(columns=["Wage", "Birth Date", "name", "nation"])
    df = one_hot_coding(df)

    return df


def scale_input(pX, df):

    df = df.drop(columns=["Value"])
    input_scaler = StandardScaler().fit(df)
    scaled_input = input_scaler.transform(pX)
    return scaled_input


def scale_target(target, df):
    """Scales Target 'y' Value"""

    y = df["Value"].values  # Target
    y = np.log(y)
    y = y.reshape(-1, 1)  # Reshape
    scaler = StandardScaler()
    y_scaler = scaler.fit(y)
    scaled_target = y_scaler.inverse_transform(target)
    return scaled_target


def human_readable_payload(value_predict):
    """Takes numpy array and returns back human readable dictionary"""

    value_log = float(np.round(value_predict, 2))
    value_stimate = float(np.round(np.exp(value_predict), 2))
    result = {
        "value_log": value_log,
        "value_money": f"{value_stimate} euros",
    }
    return result


def predict(pX):
    """Takes weight and predicts height"""

    clf = load_model()  # loadmodel
    df = clean_data()
    scaled_input_result = scale_input(pX, df)  # scale feature input
    scaled_height_prediction = clf.predict(scaled_input_result)  # scaled prediction
    value_predict = scale_target(scaled_height_prediction, df)
    # payload = human_readable_payload(height_predict)
    # predict_log_data = {
    #    "weight": weight,
    #    "scaled_input_result": scaled_input_result,
    #    "scaled_height_prediction": scaled_height_prediction,
    #    "height_predict": height_predict,
    #    "human_readable_payload": payload,
    # }
    # logging.debug(f"Prediction: {predict_log_data}")
    result = human_readable_payload(value_predict)
    return result
