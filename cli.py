#!/usr/bin/env python

"""MLOps Library"""

import click
from mlib import predict
import json
import pandas as pd


@click.command()
@click.option(
    "--skills",
    prompt="Fifa Player skills",
    help="Pass the skills of a Fifa player to predict the Value",
)
def predictcli(skills):
    """Predicts Value of an Fifa player based on skills"""
    data_to_predict = json.loads(skills)
    data_to_predict = pd.DataFrame(data_to_predict)

    result = predict(data_to_predict)
    value_log = result["value_log"]
    if float(value_log) > 15:
        click.echo(click.style(result, bg="green", fg="black"))
    else:
        click.echo(click.style(result, bg="red", fg="black"))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    predictcli()

# Example
# python cli.py --skills '
#   [{\"overallrating\": 75,
#  \"potencial\": 76,
#  \"height\": 174,
#  \"weight\": 67,
#  \"Age\": 26,
#  \"Contract Length\": 2024,
#  \"Ball Control\": 78.0,
#  \"Dribbling\": 81.0,
#  \"Marking\": 32.0,
#  \"Slide Tackle\": 26.0,
#  \"Stand Tackle\": 30.0,
#  \"Aggression\": 61.0,
#  \"Reactions\": 73.0,
#  \"Att. Position\": 72.0,
#  \"Interceptions\": 49.0,
#  \"Vision\": 70.0,
#  \"Composure\": 79.0,
#  \"Crossing\": 66.0,
#  \"Short Pass\": 71.0,
#  \"Long Pass\": 63.0,
#  \"Acceleration\": 83.0,
#  \"Stamina\": 76.0,
#  \"Strength\": 55.0,
#  \"Balance\": 86.0,
#  \"Sprint Speed\": 75.0,
#  \"Agility\": 89.0,
#  \"Jumping\": 76.0,
#  \"Heading\": 50.0,
#  \"Shot Power\": 71.0,
#  \"Finishing\": 76.0,
#  \"Long Shots\": 73.0,
#  \"Curve\": 73.0,
#  \"FK Acc.\": 69.0,
#  \"Penalties\": 72.0,
#  \"Volleys\": 70.0,
#  \"GK Positioning\": 15,
#  \"GK Diving\": 9,
#  \"GK Handling\": 12,
#  \"GK Kicking\": 8,
#  \"GK Reflexes\": 14,
#  \"Preferred Foot_Left\": 0,
#  \"Preferred Foot_Right\": 1,
#  \"Player Work Rate_High / High\": 0,
#  \"Player Work Rate_High / Low\": 0,
#  \"Player Work Rate_High / Medium\": 1,
#  \"Player Work Rate_Low / High\": 0,
#  \"Player Work Rate_Low / Low\": 0,
#  \"Player Work Rate_Low / Medium\": 0,
#  \"Player Work Rate_Medium / High\": 0,
#  \"Player Work Rate_Medium / Low\": 0,
#  \"Player Work Rate_Medium / Medium\": 0,
#  \"position_zone_ATTACKING\": 0,
#  \"position_zone_DEFENDING\": 0,
#  \"position_zone_GOALKEEPER\": 0,
#  \"position_zone_MIDFIELD\": 1}]'
#
# python cli.py --skills '
# [{"overallrating": 75,
# "potencial": 76,
# "height": 174,
# "weight": 67,
# "Age": 26,
# "Contract Length": 2024,
# "Ball Control": 78.0,
# "Dribbling": 81.0,
# "Marking": 32.0,
# "Slide Tackle": 26.0,
# "Stand Tackle": 30.0,
# "Aggression": 61.0,
# "Reactions": 73.0,
# "Att. Position": 72.0,
# "Interceptions": 49.0,
# "Vision": 70.0,
# "Composure": 79.0,
# "Crossing": 66.0,
# "Short Pass": 71.0,
# "Long Pass": 63.0,
# "Acceleration": 83.0,
# "Stamina": 76.0,
# "Strength": 55.0,
# "Balance": 86.0,
# "Sprint Speed": 75.0,
# "Agility": 89.0,
# "Jumping": 76.0,
# "Heading": 50.0,
# "Shot Power": 71.0,
# "Finishing": 76.0,
# "Long Shots": 73.0,
# "Curve": 73.0,
# "FK Acc.": 69.0,
# "Penalties": 72.0,
# "Volleys": 70.0,
# "GK Positioning": 15,
# "GK Diving": 9,
# "GK Handling": 12,
# "GK Kicking": 8,
# "GK Reflexes": 14,
# "Preferred Foot_Left": 0,
# "Preferred Foot_Right": 1,
# "Player Work Rate_High / High": 0,
# "Player Work Rate_High / Low": 0,
# "Player Work Rate_High / Medium": 1,
# "Player Work Rate_Low / High": 0,
# "Player Work Rate_Low / Low": 0,
# "Player Work Rate_Low / Medium": 0,
# "Player Work Rate_Medium / High": 0,
# "Player Work Rate_Medium / Low": 0,
# "Player Work Rate_Medium / Medium": 0,
# "position_zone_ATTACKING": 0,
# "position_zone_DEFENDING": 0,
# "position_zone_GOALKEEPER": 0,
# "position_zone_MIDFIELD": 1}]'
