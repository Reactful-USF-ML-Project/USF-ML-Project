import tensorflow as tf
import numpy as np
import file_parser as matrix_generator
feature_name_from_input_fn = 'test'
vocabulary_feature_column = tf.feature_column.categorical_column_with_vocabulary_list( key=feature_name_from_input_fn, vocabulary_list=["kitchenware", "electronics", "sports"])
print(vocabulary_feature_column)