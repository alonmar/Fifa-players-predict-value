[![MLOPs fifa value predict Github Actions](https://github.com/alonmar/Fifa-players-predict-value/actions/workflows/main.yml/badge.svg)](https://github.com/alonmar/Fifa-players-predict-value/actions/workflows/main.yml)

# MLOps Fifa players predict value


## Assets in repo

* `requirements.txt`:  [View requirements.txt](https://github.com/alonmar/Fifa-players-predict-value/blob/main/requirements.txt)
* `Futbol_Predictions_Export_Model.ipynb`: [View eda.ipynb](https://github.com/alonmar/Fifa-players-predict-value/blob/main/Futbol_Predictions_Export_Model.ipynb) EDA and Export model
* `data_fifa_players.json`: [View data](https://github.com/alonmar/Fifa-players-predict-value/blob/main/webscrapi_fifa_players/data_fifa_players.json) Data scraping
* `model.joblib`: [View model.joblib](https://github.com/alonmar/Fifa-players-predict-value/blob/main/model.joblib) Exported Model 
* `app.py`:  [View app.py](https://github.com/alonmar/Fifa-players-predict-value/blob/main/app.py) Flask api
* `mlib.py`:  [View mlib.py](https://github.com/alonmar/Fifa-players-predict-value/blob/main/mlib.py) Model Handling Library
* `cli.py`: [View cli.py](https://github.com/alonmar/Fifa-players-predict-value/blob/main/cli.py) Console predict
* `test_mlib.py`:  [View test_mlib.py](https://github.com/alonmar/Fifa-players-predict-value/blob/main/test_mlib.py) Unit test
* `utilscli.py`: [View utilscli.py](https://github.com/alonmar/Fifa-players-predict-value/blob/main/utilscli.py) Utility Belt
* `Dockerfile`: [View Dockerfile](https://github.com/alonmar/Fifa-players-predict-value/blob/main/Dockerfile) 
* `Makefile`: [View Makefile](https://github.com/alonmar/Fifa-players-predict-value/blob/main/Makefile) 
* `main.yml`: [View main.yml](https://github.com/alonmar/Fifa-players-predict-value/blob/main/.github/workflows/main.yml) Github Actions
* `webscrapi_fifa_players`: [View webscrapi_fifa_players](https://github.com/alonmar/Fifa-players-predict-value/tree/main/webscrapi_fifa_players) Scrapy proyect

## CLI Tools

There are two cli tools.  First, the main `cli.py` is the endpoint that serves out predictions.
To predict the height of an MLB player you use the following: *(if you don't run on Windows delete the backslash "`\`")*

`$ python ./cli.py --skills '[{\"overallrating\": 75, \"potencial\": 76, \"height\": 174, \"weight\": 67, \"Age\": 26, \"Contract Length\": 2024, \"Ball Control\": 78.0, \"Dribbling\": 81.0, \"Marking\": 32.0, \"Slide Tackle\": 26.0, \"Stand Tackle\": 30.0, \"Aggression\": 61.0, \"Reactions\": 73.0, \"Att. Position\": 72.0, \"Interceptions\": 49.0, \"Vision\": 70.0, \"Composure\": 79.0, \"Crossing\": 66.0, \"Short Pass\": 71.0, \"Long Pass\": 63.0, \"Acceleration\": 83.0, \"Stamina\": 76.0, \"Strength\": 55.0, \"Balance\": 86.0, \"Sprint Speed\": 75.0, \"Agility\": 89.0, \"Jumping\": 76.0, \"Heading\": 50.0, \"Shot Power\": 71.0, \"Finishing\": 76.0, \"Long Shots\": 73.0, \"Curve\": 73.0, \"FK Acc.\": 69.0, \"Penalties\": 72.0, \"Volleys\": 70.0, \"GK Positioning\": 15, \"GK Diving\": 9, \"GK Handling\": 12, \"GK Kicking\": 8, \"GK Reflexes\": 14, \"Preferred Foot_Left\": 0, \"Preferred Foot_Right\": 1, \"Player Work Rate_High / High\": 0, \"Player Work Rate_High / Low\": 0, \"Player Work Rate_High / Medium\": 1, \"Player Work Rate_Low / High\": 0, \"Player Work Rate_Low / Low\": 0, \"Player Work Rate_Low / Medium\": 0, \"Player Work Rate_Medium / High\": 0, \"Player Work Rate_Medium / Low\": 0, \"Player Work Rate_Medium / Medium\": 0, \"position_zone_ATTACKING\": 0, \"position_zone_DEFENDING\": 0, \"position_zone_GOALKEEPER\": 0, \"position_zone_MIDFIELD\": 1}]'`

![predict-value](https://user-images.githubusercontent.com/36181705/148481545-390305d2-3428-4980-99ed-e85627eb0117.png)


The second cli tool is `utilscli.py` and this perform model retraining, and could serve as the entry point to do more things.
For example, this version doesn't change the default `model_name`, but you could add that as an option by forking this repo.

`$ python ./utilscli.py retrain --tsize 0.2`

![model-retraining](https://user-images.githubusercontent.com/36181705/148481027-cb825882-ae04-4df1-b9ec-dcc3a08dbb5e.png)


## Flask Microservice

The Flask ML Microservice can be run many ways.

### Containerized Flask Microservice Locally

You can run the Flask Microservice as follows with the commmand:

`$ python app.py runserver`

![flask-local](https://user-images.githubusercontent.com/36181705/148481892-c15c9703-c27a-494d-9bfb-324625af5fd1.png)

After run flask to serve a prediction against the application, run the [predict.sh](https://github.com/alonmar/Fifa-players-predict-value/blob/main/predict.sh).

For the bourne shell: 

`sh ./predict.sh`

For bash:

`bash ./predict.sh`

For windows:

https://stackoverflow.com/questions/26522789/how-to-run-sh-on-windows-command-prompt

```
$ bash ./predict.sh                             
Port: 8080
{
  "prediction": {
    "value_log": 15.66,
    "value_money": "6330106.07 euros"
  }
}
```

### Containerized Flask Microservice

Here is an example of how to build the container and run it locally, this is the contents of [run_docker.sh](https://github.com/alonmar/Fifa-players-predict-value/blob/main/run_docker.sh)

```
#!/usr/bin/env bash

# Build image
docker build --tag=alonmar/mlops-value_fifa_players . 

# List docker images
docker image ls

# Run flask app
docker run -p 127.0.0.1:8080:8080 alonmar/mlops-value_fifa_players
```

## Github Actions

When you push on main Github detect this [main.yml](https://github.com/alonmar/Fifa-players-predict-value/blob/main/.github/workflows/main.yml) and automatically build Container via Github Actions

![github-actions](https://user-images.githubusercontent.com/36181705/148483487-f80103d8-65a6-4524-807c-a26bbec590a6.png)


## Scrap the data

* Step 1: Clone the repo 

`$ git clone https://github.com/alonmar/Fifa-players-predict-value.git`

* Step 2: Install requirements.txt

`$ pip install -r requirements.txt`

* Step 3: move to dir webscrapi_fifa_players 

`$ cd webscrapi_fifa_players`

* Step 4: Start the crawler 

`$ scrapy crawl skills`

And wait until webscraping finishes 🎉
