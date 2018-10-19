import tensorflow as tf

# We will use NumPy matrices in TensorFlow

import csv
import numpy
from datetime import datetime

def update_dict(dictionary, object_type, object_id):
    if object_type not in dictionary:
        dictionary.update({object_type:[]})
        dictionary[object_type].append(object_id)
    elif object_id not in dictionary[object_type]:
        dictionary[object_type].append(object_id)

def get_session_length(start, end):
    st = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    et = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    return (et - st).seconds

def place_in_current_session(key,value,current_session,possible_values,map_to_session_index):
    update_dict(possible_values, object_key, object_value)

    if key == "page":
        page_count = current_session[map_to_session_index['page_count']]
        if page_count is None:
            current_session[map_to_session_index['page_count']] = 0

        current_session[map_to_session_index['page_count']] += 1

    elif key in map_to_session_index:
        position_in_possibles = possible_values[object_key].index(value)
        current_session[map_to_session_index[key]] = position_in_possibles

# Ordering of a session so far (used in map_to_session_index):
# [ average time on page, region, type, device, page count, reaction combination, goal combination, session_length]

with open('./results-20181008-130002 - results-20181008-130002.csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    session_ids = []
    matrix = []
    matrix_index = -1
    start_time = -1
    end_time = -1
    possible_values = {}
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
    for row in csv_reader:
        if line_count == 0:
            labels = [] 
            for l in row: 
                labels.append(l)
        else:
            sid = row[2]

            if sid in session_ids:
                current_session = matrix[matrix_index]
                time = row[0]
                if time < start_time:
                    start_time = time
                elif time > end_time:
                    end_time = time

                object_key = row[3]
                object_value = row[4]
                place_in_current_session(object_key,object_value,current_session,possible_values,map_to_session_index)

            else:
                if matrix_index > 0:
                    last_session = matrix[matrix_index - 1]
                    session_length = get_session_length(start_time, end_time)
                    last_session[map_to_session_index['session_length']] = session_length
                    page_count = last_session[map_to_session_index['page_count']]

                    if session_length > 0 and page_count > 0:    
                        last_session[map_to_session_index['avg_time_per_page']] = session_length / page_count
                    else:
                        last_session[map_to_session_index['avg_time_per_page']] = 0
                matrix_index += 1
                session_ids.append(sid)

                a = numpy.empty(len(map_to_session_index), dtype=object)
                matrix.append(a)
                # check if time is smaller than min or greater than max
                time = row[0]
                start_time = time
                end_time = time

                # use object key val pair to
                object_key = row[3]
                object_value = row[4]
                update_dict(possible_values, object_key, object_value)
                current_session = matrix[matrix_index]
                current_session[map_to_session_index['reaction']] = 0
                current_session[map_to_session_index['goal']] = 0
                if object_key == "page":
                    current_session[map_to_session_index['page_count']] = 1
                else:
                    current_session[map_to_session_index['page_count']] = 0
                    if object_key in map_to_session_index:
                        value = possible_values[object_key].index(object_value)
                        current_session[map_to_session_index[object_key]] = value
 
        line_count += 1
    print("Processed " + str(line_count) + " lines.")
    x = 0
    # for e in possible_values:
    #     print e
    #     for x in possible_values[e]:
    #         print "\t" + x
    # print(matrix)

    # print(labels) 
print(len(matrix))
new_matrix = []
for session in matrix:
	if None not in session:
		new_matrix.append(session)


m2 = numpy.array(new_matrix, dtype=numpy.int32)

print(type(m2))

t2 = tf.convert_to_tensor(m2, dtype=tf.float32)

print(t2)






