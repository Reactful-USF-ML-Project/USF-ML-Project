import tensorflow as tf
import numpy
import file_parser as matrix_generator

(matrix,possible_values) = matrix_generator.get_matrix()
# Stuff to look into
# https://www.tensorflow.org/guide/feature_columns
# https://stackoverflow.com/questions/46834680/creating-many-feature-columns-in-tensorflow
new_matrix = []
for session in matrix:
	if None not in session:
		new_matrix.append(session)


# Creating feature columns for each categorical type

region = tf.feature_column.categorical_column_with_vocabulary_list("region", possible_values["region"])
customer_type = tf.feature_column.categorical_column_with_vocabulary_list("type", possible_values["type"])
device = tf.feature_column.categorical_column_with_vocabulary_list("device", possible_values["device"])
reaction = tf.feature_column.categorical_column_with_vocabulary_list("reaction", possible_values["reaction"])
goal = tf.feature_column.categorical_column_with_vocabulary_list("goal", possible_values["goal"])

base_columns = [region, customer_type, device, reaction, goal]
m = tf.estimator.LinearClassifier(
    model_dir="./model", feature_columns=base_columns)
print(m)
print(type(m))
print(type(new_matrix))

print(numpy.array(new_matrix).shape)
# numpy_array = numpy.array(new_matrix, dtype=numpy.int32)

# print(type(numpy_array))

# tensor = tf.convert_to_tensor(numpy_array, dtype=tf.float32)

# print(tensor)






