import itertools
import bigquery as matrix_generator
import numpy
import tensorflow as tf
# """ maching_learning.py: Gets TensorFlow-friendly data and completes iteration of training in TensorFlow. """

__author__ = "Nick Perez", "Kelsea Flores", "John Murray"


# """ Gets TensorFlow friendly data by calling matrix_generator.get_matrix() on the CSV file. """
(features, possible_values, labels) = matrix_generator.get_matrix()
feature_length = len(features['page_count'])

# """ When called, finds the longest array of values and ensures all other
#     arrays are the same length. Replaces all empty values with an empty string.

#     Arguments:
#      - v:
#             Input array to work on
#      - typer:
#             Typecode or data-type to which the array is cast

#     Return:
#      - A new array of the same shape as the input array with the order
#        given by typer

#     Sources:
#      - https://stackoverflow.com/questions/38619143/convert-python-sequence-to-numpy-array-filling-missing-values
# """


def get_max(v, typer):
    max_len = numpy.argmax(v)
    return numpy.hstack(numpy.insert(v, range(1, len(v)+1), [['']*(max_len-len(i)) for i in v])).astype(typer).reshape(len(v), max_len)


# """ Converts the data returned from matrix_generator.get_matrix() into
#     a dataset.

#     Arguments:
#      - batch_size:
#             An integer indicating the desired batch size

#     Return:
#      - A dataset

#     Sources:
#      - https://stackoverflow.com/questions/48697799/tensorflow-feature-column-for-variable-list-of-values
# """


def input_evaluation_set(batch_size, is_evaluation_set):
    train_set_size = 9
    slice_training = slice(0 if is_evaluation_set else -1, -
                           train_set_size, 1 if is_evaluation_set else -1)
    map_to_session_index = {
        'avg_time_per_page': 0,
        'region': 1,
        'type': 2,
        'device':  3,
        'page_count': 4,
        'reaction': 5,
        'goal': 6,
        'session_length': 7
    }
    t_features = {
        'region': features['region'][slice_training],
        'type':  features['type'][slice_training],
        'device': features['device'][slice_training],
        # Needed to be filled with empty '' Need to figure out a way around this
        'reaction': get_max(features['reaction'], 'str')[slice_training],
        # 'goal': get_max(features['goal'], 'str')[slice_training],
        'session_length': features['session_length'][slice_training],
        'avg_time_per_page': features['avg_time_per_page'][slice_training],
        'page_count': features['page_count'][slice_training]
    }

    # """ Iterates through list of completed reactions and appends the index of each
    #     reaction in the list of reactions in the possible_values dictionary.
    # """
    new_labels = []
    for label in labels:
        new_labels.append(possible_values['reaction'].index(label))
    # print(new_labels)

    # """ Converts the inputs to a dataset. """
    dataset = tf.data.Dataset.from_tensor_slices(
        (dict(t_features), new_labels[slice_training]))
    print("Created " + ("Evaluation" if is_evaluation_set else "Training") + " Set...")
    # return features
    return dataset.batch(batch_size)

# print(input_evaluation_set(0))


# """ Creating feature columns for each categorical type. """
region = tf.feature_column.indicator_column(
    tf.feature_column.categorical_column_with_vocabulary_list("region", possible_values["region"]))
customer_type = tf.feature_column.indicator_column(
    tf.feature_column.categorical_column_with_vocabulary_list("type", possible_values["type"]))
device = tf.feature_column.indicator_column(
    tf.feature_column.categorical_column_with_vocabulary_list("device", possible_values["device"]))
reaction = tf.feature_column.indicator_column(
    tf.feature_column.categorical_column_with_vocabulary_list("reaction", possible_values["reaction"]))
# goal = tf.feature_column.indicator_column(
# tf.feature_column.categorical_column_with_vocabulary_list("goal", possible_values["goal"]))
session_length = tf.feature_column.numeric_column(
    "session_length")
avg_time_per_page = tf.feature_column.numeric_column(
    "avg_time_per_page")
page_count = tf.feature_column.numeric_column(
    "page_count")


# SEE: https://www.tensorflow.org/tutorials/estimators/linear

# """ Trains a model using all of the features in base_columns. """
base_columns = [region, customer_type, device, reaction,
                session_length, avg_time_per_page, page_count]
m = tf.estimator.LinearClassifier(
    model_dir="./model", feature_columns=base_columns)
iterations = 1
while (iterations < 1000):
    print('Running the %s iteration' % str(iterations))
    batch_size = iterations * 10
    classifier = tf.estimator.DNNClassifier(
        model_dir="./model",
        feature_columns=base_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        # The model must choose between possible Reaction IDs.
        n_classes=len(possible_values['reaction']))

    print("Training...")

    classifier.train(
        input_fn=lambda: input_evaluation_set(batch_size, True),
        steps=(iterations*20))

    result = classifier.evaluate(
        lambda: input_evaluation_set(batch_size, False))

    for key, value in sorted(result.items()):
        print('%s: %0.2f' % (key, value))

    iterations += 1


# """
#     Additional resources:
#      - https://stackoverflow.com/questions/46834680/creating-many-feature-columns-in-tensorflow
#      - https://www.tensorflow.org/guide/feature_columns
# """
