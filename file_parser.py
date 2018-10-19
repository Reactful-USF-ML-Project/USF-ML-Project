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

# [ start time, end time, average time on page, country, 
#   region, type, device, page count, reaction combination, goal combination, session_length]

with open('../../../Downloads/results-20181008-130002 - results-20181008-130002.csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    session_ids = []
    matrix = []
    matrix_index = -1
    start_time = -1
    end_time = -1
    possible_values = {}
    key_dict = {'country': 3, 'region': 4, 'type': 5, 'device': 6, 'reaction': 8, 'goal': 9}
    for row in csv_reader:
        if line_count == 0:
            labels = [] 
            for l in row: 
                labels.append(l)
        else:
            sid = row[2]

            if sid in session_ids:
                time = row[0]
                if time < start_time:
                    start_time = time
                    matrix[matrix_index][0] = start_time
                elif time > end_time:
                    end_time = time
                    matrix[matrix_index][1] = end_time

                object_type = row[3]
                object_id = row[4]
                update_dict(possible_values, object_type, object_id)

                if object_type == "page":
                    matrix[matrix_index][7] += 1
                elif object_type in key_dict:
                    array_index = key_dict[object_type]
                    value = possible_values[object_type].index(object_id)
                    matrix[matrix_index][array_index] = value

            else:
                if matrix_index > 0:
                    st = matrix[matrix_index-1][0]
                    et = matrix[matrix_index-1][1]
                    session_length = get_session_length(st, et)
                    matrix[matrix_index-1][10] = session_length
                    page_count = matrix[matrix_index-1][7]
                    if session_length > 0 and page_count > 0:
                        matrix[matrix_index-1][2] = session_length/page_count
                    else:
                        matrix[matrix_index-1][2] = 0
                matrix_index += 1
                session_ids.append(sid)

                a = numpy.empty(11, dtype=object)
                matrix.append(a)
                # check if time is smaller than min or greater than max
                time = row[0]
                start_time = time
                end_time = time
                matrix[matrix_index][0] = start_time
                matrix[matrix_index][1] = end_time

                # use object key val pair to
                object_type = row[3]
                object_id = row[4]
                update_dict(possible_values, object_type, object_id)

                if object_type == "page":
                    matrix[matrix_index][7] = 1
                else:
                    matrix[matrix_index][7] = 0
                    if object_type in key_dict:
                        array_index = key_dict[object_type]
                        value = possible_values[object_type].index(object_id)
                        matrix[matrix_index][array_index] = value
 
        line_count += 1
    print("Processed " + str(line_count) + " lines.")
    x = 0
    # for e in possible_values:
    #     print e
    #     for x in possible_values[e]:
    #         print "\t" + x
    # print(matrix)
    for a in matrix:
            result = ", ".join(map(str, a))
            print result
    # print(labels)