from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import pandas as pd

import mlib

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route("/")
def home():
    html = f"<h3>Predict the Value From skills of FIFA Players</h3>"
    return html.format(format)


@app.route("/predict", methods=["POST"])
def predict():
    """Predicts the Value of FIFA Players"""

    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    df = pd.DataFrame(json_payload)
    prediction = mlib.predict(df)
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
