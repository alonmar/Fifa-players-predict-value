"""MLOps Library"""

import numpy as np
import pandas as pd

# from sklearn.linear_model import Ridge
import joblib

# from sklearn.model_selection import train_test_split

# Models
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

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
    df["height"] = df["height"].str.extract("(\\d+)").astype(int)
    # kg
    df["weight"] = df["weight"].str.extract("(\\d+)").astype(int)
    # euros
    df["Value"] = pd.to_numeric(df["Value"].str.replace("€|\\.", "", regex=True))
    df["Wage"] = pd.to_numeric(df["Wage"].str.replace("€|\\.", "", regex=True))

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


def retrain(tsize=0.2, model_name="model.joblib"):
    """Retrains the model

    See this notebook: Baseball_Predictions_Export_Model.ipynb
    """
    df = clean_data()
    y = df["Value"].values  # Target
    # Transform to log
    y = np.log(y)
    y = y.reshape(-1, 1)
    X = df.drop(columns=["Value"])  # Feature(s)

    scaler = StandardScaler()
    X_scaler = scaler.fit(X)
    X = X_scaler.transform(X)
    y_scaler = scaler.fit(y)
    y = y_scaler.transform(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=tsize, random_state=3
    )

    parameters = {
        "param_distributions": {
            "max_depth": [3, 6, 10],
            "learning_rate": [0.01, 0.05, 0.1, 0.3, 0.5],
            "n_estimators": [100, 500, 1000],
            "colsample_bytree": [0.7, 0.5],
        },
        "scoring": "neg_mean_squared_error",
        "verbose": 3,
        "n_jobs": -1,
    }

    xgb_model = XGBRegressor(seed=20)
    xgb_grid = RandomizedSearchCV(estimator=xgb_model, **parameters)
    model = xgb_grid.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    predictions = model.predict(X_test)

    logging.debug(f"fit_model.best_params: {model.best_params_}")
    rmse_xgb_reg = mean_squared_error(
        y_scaler.inverse_transform(y_test),
        y_scaler.inverse_transform(predictions.reshape(-1, 1)),
        squared=False,
    )

    print(f"The RMSE for xgb_reg is: {rmse_xgb_reg}")
    print(model.best_params_)
    # joblib.dump(model, model_name)
    return accuracy, model_name


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
