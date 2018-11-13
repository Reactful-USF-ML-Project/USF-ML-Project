""" maching_learning.py: Gets TensorFlow-friendly data and completes iteration of training in TensorFlow. """

__author__      = "Nick Perez", "Kelsea Flores", "John Murray"

import tensorflow as tf
import numpy
import file_parser as matrix_generator
import itertools

""" Gets TensorFlow friendly data by calling matrix_generator.get_matrix() on the CSV file. """
(features,possible_values, labels) = matrix_generator.get_matrix()
feature_length = len(features['page_count'])

""" When called, finds the longest array of values and ensures all other
    arrays are the same length. Replaces all empty values with an empty string. 

    Arguments: 
     - v:
            Input array to work on
     - typer: 
            Typecode or data-type to which the array is cast

    Return: 
     - A new array of the same shape as the input array with the order
       given by typer

    Sources: 
     - https://stackoverflow.com/questions/38619143/convert-python-sequence-to-numpy-array-filling-missing-values
"""
def get_max(v,typer): 
    max_len = numpy.argmax(v)
    return numpy.hstack(numpy.insert(v, range(1, len(v)+1),[['']*(max_len-len(i)) for i in v])).astype(typer).reshape(len(v), max_len)


""" Converts the data returned from matrix_generator.get_matrix() into 
    a dataset. 

    Arguments:
     - batch_size: 
            An integer indicating the desired batch size

    Return: 
     - A dataset

    Sources:
     - https://stackoverflow.com/questions/48697799/tensorflow-feature-column-for-variable-list-of-values
"""
def input_evaluation_set(batch_size):
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
        'region': features['region'],
        'type':  features['type'],
        'device': features['device'],
        'reaction': get_max(features['reaction'],'str'), # Needed to be filled with empty '' Need to figure out a way around this
        'goal': get_max(features['goal'], 'str'),
        'session_length': features['session_length']
    }
    
	# matrix_index = 0
	# for feature in features:
	# 	for key in features.keys():
 #                    print(features[key][matrix_index])
 #                    features[key][matrix_index][0] += session[map_to_session_index[key]][0]
	# 	matrix_index += 1
	# print(features)

	# for key in features.keys():
		# features[key]=tf.convert_to_tensor(features[key], dtype=tf.string)
	
    """ Iterates through list of completed reactions and appends the index of each
        reaction in the list of reactions in the possible_values dictionary. 
    """
    new_labels=[]
	for label in labels:
		new_labels.append(possible_values['reaction'].index(label))
	# print(new_labels)

    """ Converts the inputs to a dataset. """
	dataset = tf.data.Dataset.from_tensor_slices((dict(t_features), new_labels))

	# return features
	return dataset.batch(batch_size)

# print(input_evaluation_set(0))

""" Creating feature columns for each categorical type. """
region = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("region", possible_values["region"]))
customer_type = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("type", possible_values["type"]))
device = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("device", possible_values["device"]))
reaction = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("reaction", possible_values["reaction"]))
goal = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("goal", possible_values["goal"]))
# session_length = tf.feature_column.numeric_column(key='session_length',default_value=possible_values['session_length'], dtype=tf.int64)


# SEE: https://www.tensorflow.org/tutorials/estimators/linear

""" Trains a model using all of the features in base_columns. """
base_columns = [region, customer_type, device, reaction, goal]
m = tf.estimator.LinearClassifier(
    model_dir="./model", feature_columns=base_columns)

classifier = tf.estimator.DNNClassifier(
	model_dir="./model",
    feature_columns=base_columns,
    # Two hidden layers of 10 nodes each.
    hidden_units=[10, 10],
    # The model must choose between possible Reaction IDs.
    n_classes=len(possible_values['reaction']))

classifier.train(
    input_fn=lambda:input_evaluation_set(100),
    steps=100)


# print(classifier)
# print(type(classifier))
# # numpy_array = numpy.array(new_matrix, dtype=numpy.int32)

# # print(type(numpy_array))

# # tensor = tf.convert_to_tensor(numpy_array, dtype=tf.float32)

# # print(tensor)

""" 
    Additional resources: 
     - https://stackoverflow.com/questions/46834680/creating-many-feature-columns-in-tensorflow
     - https://www.tensorflow.org/guide/feature_columns
"""