# Reactful USF ML Project

Machine Learning of past Reactful data with Tensorflow in the Google Cloud Platform.

# Basic Installation Instructions

For this project we used Tensorflow, which is pretty much the undeclared standard for machine learning that allows you to get up and running with machine learning in a *relatively pain-free* way. There is more info located in [SETUP.md](SETUP.md) so give that a look if you don't already have your Tensorflow environment setup.

1. [Install Tensorflow](https://www.tensorflow.org/install/) We followed the [pip installer for Python 2.7](https://www.tensorflow.org/install/pip)
2. If you need any more help a more detailed guide [I wrote is here in SETUP.md](SETUP.md)



# Overview of files in this repository

- `completed_reactions.csv` This was our initial dataset that we used to train with where the format of the file is the exact dump of the tables as stored in the corresponding BigQuery database that requires a bunch of parsing to get into a format that Tensorflow can handle.
- `file_parser.py` This is what converts that completed_reactions CSV file into a format that Tensorflow can handle. Outputting `features, possible_values, completed_reactions`
  - `features` an in-memory dictionary with the interesting data labels as keys and the data values as an index into the array of sessions as values I.E : ```{ 'region' : [ 'region code for session #1', 'region code for session #2' ] }```
  - `possible_values` an in-memory dictionary with the interesting data labels as keys and a unique set of all data values as an index into an array to keep track of all of the possible values that these data points can take I.E : ``` { 'region': [ 'region code #1', 'region code #2' ] }```
  - `completed_reactions` an array of the last reaction (the completed reaction) IDs that corresponds to the expected output of what reaction was completed.
- `ex.sql` This is the SQL query that was made to pull down all of the relevant information needed to train with from the BigQuery database.
- `bigquery.py` This is what pulls down data directly from BigQuery using the aforementioned SQL query. It then Post processes the results of those results to generate the same output as `file_parser.py` as well as transform any data that is in an intermediary format such as relativizing `start_time` and `end_time` to simply correspond to `session_length`
- `machine_learning.py` This is what actually performs the model setup, training and prediction and contains within all of the machine learning related tasks.