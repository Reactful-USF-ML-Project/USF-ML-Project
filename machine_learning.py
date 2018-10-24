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

print(type(new_matrix))

print(numpy.array(new_matrix).shape)
# numpy_array = numpy.array(new_matrix, dtype=numpy.int32)

# print(type(numpy_array))

# tensor = tf.convert_to_tensor(numpy_array, dtype=tf.float32)

# print(tensor)






