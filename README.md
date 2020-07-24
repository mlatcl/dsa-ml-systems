# dsa-ml-systems
Repo for teaching materials related to the Data Science Africa course Machine Learning Systems

## Running the Streaming Example

### Prerequisites
You'll need to have docker-compose installed to run the examples.

You can just run
```pip install -r requirements.txt```
from this folder to install the Python libraries you should need.

## Starting the Kafka Server

The first step is to spin up the Zookeeper and Kafka servers that are the backend to the streaming example.
This is done using docker-compose with the ```conf-docker-compose.yml``` file.

```
docker-compose -f conf-docker-compose.yml up
```

## Starting the Faust Worker

The actual mechanism we use to control the kafka topics and sending is the python library Faust.

You'll need to start a worker node for Faust that will process requests to send data to the Kafka topics.

```
faust -A dsa_streaming worker -l info
```

## Sending data to the Kafka topics

Now that we have the server and worker running, we can send data to it.
Faust handles the creation of topics automatically when we send data to them, so we can go ahead and start sending.

In a new terminal, let's populate our first topic, 'state_pops' with the state populations so that we can compute the per capita COVID cases in each state.

```
python write_populations_to_stream.py
```

You should (in the terminal we ran the Faust worker from), print statements showing the updated populations and per capita cases (which would be zero right now as we haven't populated any of them.)

This file reads in the populations.csv file and writes each row to the stream individually. In a production setting, you would want to do this in batch mode but this is helpfully slow as it lets us see individual cases being processed.

Lets do the same now (in a new terminal, while the populations script runs), for the COVID cases themselves.

```
python write_cases_to_stream.py
```

You should see the cases and cases per capita updating here.

If you look inside the dsa_streaming.py file, you'll see that we've written our own "join" of sorts, that keeps the cases_per_capita table updated when either the cases or populations tables get updated.


