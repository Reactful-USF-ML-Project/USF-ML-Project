# Reactful USF ML Project

Machine Learning of past Reactful data with Tensorflow in the Google Cloud Platform.

# Basic Installation Instructions

For this project we used Tensorflow, which is pretty much the undeclared standard for machine learning that allows you to get up and running with machine learning in a *relatively pain-free* way. There is more info located in [SETUP.md](SETUP.md) so give that a look if you don't already have your Tensorflow environment setup.

1. [Install Tensorflow](https://www.tensorflow.org/install/) We followed the [pip installer for Python 2.7](https://www.tensorflow.org/install/pip)
2. If you need any more help a more detailed guide [I wrote is here in SETUP.md](SETUP.md)



# Overview of files in this repository

- [`completed_reactions.csv`](completed_reactions.csv) This was our initial dataset that we used to train with where the format of the file is the exact dump of the tables as stored in the corresponding BigQuery database that requires a bunch of parsing to get into a format that Tensorflow can handle.
- [`file_parser.py`](file_parser.py) This is what converts that completed_reactions CSV file into a format that Tensorflow can handle. Outputting `features, possible_values, completed_reactions`
  - `features` an in-memory dictionary with the interesting data labels as keys and the data values as an index into the array of sessions as values I.E : ```{ 'region' : [ 'region code for session #1', 'region code for session #2' ] }```
  - `possible_values` an in-memory dictionary with the interesting data labels as keys and a unique set of all data values as an index into an array to keep track of all of the possible values that these data points can take I.E : ``` { 'region': [ 'region code #1', 'region code #2' ] }```
  - `completed_reactions` an array of the last reaction (the completed reaction) IDs that corresponds to the expected output of what reaction was completed.
- [`ex.sql`](ex.sql) This is the SQL query that was made to pull down all of the relevant information needed to train with from the BigQuery database.
- [`bigquery.py`](bigquery.py) This is what pulls down data directly from BigQuery using the aforementioned SQL query. It then Post processes the results of those results to generate the same output as `file_parser.py` as well as transform any data that is in an intermediary format such as relativizing `start_time` and `end_time` to simply correspond to `session_length`
- [`machine_learning.py`](machine_learning.py) This is what actually performs the model setup, training and prediction and contains within all of the machine learning related tasks.

# Machine Learning

The machine learning itself was definitely the most difficult task so it will be discussed in depth here.

1. We get  `features, possible_values, completed_reactions` either from [`file_parser.py`](file_parser.py) or [`bigquery.py`](bigquery.py) as both have the same API they are interchangeable they only pull their data from different sources as the name of each respective file suggests.
2. [We setup](machine_learning.py#L95) our model using [feature columns](https://www.tensorflow.org/guide/feature_columns)
   1. `region`, `customer_type`, `device` and `reaction` all are what is called [categorical columns](https://www.tensorflow.org/guide/feature_columns#categorical_vocabulary_column) where their values are a finite set of possible strings which Tensorflow attempts to find the relationship between.
   2. `session_length`, `avg_time_per_page` and `page_count` all are what is called numeric columns where their values are a single numeric value
3. [We define the estimator we are going to use](machine_learning.py#L120) in this case a `LinearClassifier` to keep things simple (This definitely can be optimized)
4. [We define the classifier we are going to use](machine_learning.py#L123) in this case a `DNNClassifier` to create a Deep Neural Network to find complex relationships between the feature columns
5. We train the data
6. We evaluate our training by making predictions on data which it has not seen before

## Functions

### `input_evaluation_set`

This is made to convert the data into Tensors that are usable by Tensorflow at the same time this also partitions the data into the training and the evaluation sets.

### `get_max`

In order to train, the data inputted can be a multidimensional array but it must be one of a consistent shape (a rectangular matrix) so this function converts a varied dimension array and outputs a rectangular matrix with missing strings containing a default empty string in its place.

## Viewing Output

The results of the training will be put into a directory called `model/` which will contain a representation of not only the results but of the model as a whole that can be used to make predictions on data formatted in the same way.

To view these results a Web based dashboard called Tensorboard can be used by invoking: `tensorboard --logdir=model/` and the results will be viewable on your [localhost:6006](http://localhost:6006/)