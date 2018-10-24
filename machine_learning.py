import tensorflow as tf
import numpy
import file_parser as matrix_generator

(matrix,possible_values, labels) = matrix_generator.get_matrix()
matrix_length = len(matrix)
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
	features = {
        'region': numpy.ndarray(shape=(matrix_length,229), dtype=int),
        'type':  numpy.ndarray(shape=(matrix_length,2), dtype=int),
        'device': numpy.ndarray(shape=(matrix_length,1), dtype=int),
        'reaction':  numpy.ndarray(shape=(matrix_length,10), dtype=int),
        'goal':  numpy.ndarray(shape=(matrix_length,9), dtype=int)
    }

	matrix_index = 0
	for session in matrix:
		features['region'][matrix_index] = numpy.array(session[map_to_session_index['region']])
		features['type'][matrix_index] = numpy.array(session[map_to_session_index['type']])
		features['device'][matrix_index] = numpy.array(session[map_to_session_index['device']])
		features['reaction'][matrix_index] = numpy.array(session[map_to_session_index['reaction']])
		features['goal'][matrix_index] = numpy.array(session[map_to_session_index['goal']])
		matrix_index += 1

	dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

	# return features
	return dataset.batch(batch_size)
# Stuff to look into
# https://www.tensorflow.org/guide/feature_columns
# https://stackoverflow.com/questions/46834680/creating-many-feature-columns-in-tensorflow

print(input_evaluation_set(0))

# Creating feature columns for each categorical type

region = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("region", possible_values["region"]))
customer_type = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("type", possible_values["type"]))
device = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("device", possible_values["device"]))
reaction = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("reaction", possible_values["reaction"]))
goal = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list("goal", possible_values["goal"]))

base_columns = [region, customer_type, device, reaction, goal]
m = tf.estimator.LinearClassifier(
    model_dir="./model", feature_columns=base_columns)




classifier = tf.estimator.DNNClassifier(
	model_dir="./model",
    feature_columns=base_columns,
    # Two hidden layers of 10 nodes each.
    hidden_units=[10, 10],
    # The model must choose between 5 classes (Reaction IDs).
    n_classes=5)




classifier.train(
    input_fn=lambda:input_evaluation_set(100),
    steps=100)





# print(classifier)
# print(type(classifier))
# # numpy_array = numpy.array(new_matrix, dtype=numpy.int32)

# # print(type(numpy_array))

# # tensor = tf.convert_to_tensor(numpy_array, dtype=tf.float32)

# # print(tensor)






