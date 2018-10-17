import csv
import numpy

def update_dict(dictionary, object_type, object_id):
    if object_type not in dictionary:
        dictionary.update({object_type:[]})
        dictionary[object_type].append(object_id)
    elif object_id not in dictionary[object_type]:
        dictionary[object_type].append(object_id)

# [ start time, end time, average time on page, country, 
#   region, type, device, page count, reaction combination, goal combination]

with open('../../../Downloads/results-20181008-130002 - results-20181008-130002.csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    session_ids = []
    matrix = []
    matrix_index = -1
    start_time = -1
    end_time = -1
    possible_values = {}
    key_dict = {'country': 3, 'region': 4, 'type': 5, 'device': 6, 'page': 7, 'reaction': 8}
    for row in csv_reader:
        if line_count == 0:
            # Create labels array
            labels = [] 
            for l in row: 
                labels.append(l)
        else:
            # Fill in the matrix
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

            else:
                matrix_index += 1
                session_ids.append(sid)

                a = numpy.empty(10, dtype=object)
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
                    # if object type is region and value is US-CA
                    # find region in dictionary, find index of US-CA in array
                    # index = value adding into array

                if object_type == "page":
                    matrix[matrix_index][7] = 1
                else:
                    matrix[matrix_index][7] = 0
 
        line_count += 1
    print("Processed " + str(line_count) + " lines.")
    x = 0
    # for e in possible_values:
    #     print e
    #     for x in possible_values[e]:
    #         print "\t" + x
    # print(matrix)
    for a in matrix:
        print a
    # print(labels)