import tensorflow as tf

#First Code Example
# We will use NumPy matrices in TensorFlow
import numpy as np   

# Define a 2x2 matrix in 3 different ways
# m1 = [[1.0, 2.0], 
#       [3.0, 4.0]]
# m2 = np.array([[1.0, 2.0], 
#                [3.0, 4.0]], dtype=np.float32)
# m3 = tf.constant([[1.0, 2.0], 
#                   [3.0, 4.0]])

# # Print the type for each matrix
# print(type(m1))
# print(type(m2))
# print(type(m3))

# # Create tensor objects out of the different types
# t1 = tf.convert_to_tensor(m1, dtype=tf.float32)
# t2 = tf.convert_to_tensor(m2, dtype=tf.float32)
# t3 = tf.convert_to_tensor(m3, dtype=tf.float32)



# #Second Code example
# # Notice that the types will be the same now
# print(type(t1))
# print(type(t2))
# print(type(t3))

# Define a 2x1 matrix
matrix1 = tf.constant([[1., 2.]])

# Define a 1x2 matrix
matrix2 = tf.constant([[1], 
                       [2]])

# Define a rank 3 tensor
myTensor = tf.constant([ [[1,2], 
                          [3,4], 
                          [5,6]], 
                         [[7,8], 
                          [9,10], 
                          [11,12]] ])

# Try printing the tensors 
print(matrix1)
print(matrix2)
print(myTensor)