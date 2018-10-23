import tensorflow as tf
import numpy
import file_parser as matrix_generator

matrix = matrix_generator.get_matrix()

new_matrix = []
for session in matrix:
	if None not in session:
		new_matrix.append(session)


numpy_array = numpy.array(new_matrix, dtype=numpy.int32)

print(type(numpy_array))

tensor = tf.convert_to_tensor(numpy_array, dtype=tf.float32)

print(tensor)






