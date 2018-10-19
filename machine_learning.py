import tensorflow as tf
import numpy
import file_parser as matrix_generator

matrix = matrix_generator.get_matrix()

new_matrix = []
for session in matrix:
	if None not in session:
		new_matrix.append(session)


m2 = numpy.array(new_matrix, dtype=numpy.int32)

print(type(m2))

t2 = tf.convert_to_tensor(m2, dtype=tf.float32)

print(t2)






