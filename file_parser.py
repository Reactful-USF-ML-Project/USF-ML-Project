import csv

with open('../../../Downloads/results-20181008-130002 - results-20181008-130002.csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    session_ids = []
    matrix = []
    matrix_index = 0
    start_time = -1
    end_time = -1
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
                print matrix[matrix_index]
                # time = row[0]
                # if time < start_time:
                #     start_time = time
                    


                # update start and end time if necessary 
            else:
                session_ids.append(sid)
                matrix.append([])
                # check if time is smaller than min or greater than max
                time = row[0]
                start_time = -1
                end_time = -1
                if start_time == -1:
                    start_time = time
                    end_time = time
                    # matrix[matrix_index][0] = start_time
                    # matrix[matrix_index][1] = end_time
                elif time < start_time:
                    start_time = time
                    matrix[matrix_index].append(start_time)
                    # matrix[matrix_index][0] = start_time
                elif time > end_time:
                    end_time = time
                    matrix[matrix_index].append(end_time)
                    # matrix[matrix_index][1] = end_time
                matrix[matrix_index].append(start_time)
                matrix[matrix_index].append(end_time)
                # add start and end time to array i in matrix 

                # add session ID to array
                matrix[matrix_index].append(sid)
                # use object key val pair to
                object_type = row[3]
                object_id = row[4]
                    # if object type is region and value is US-CA
                    # find region in dictionary, find index of US-CA in array
                    # index = value adding into array


                # matrix[matrix_index].append(sid)
                # session_ids.append(sid)
                matrix_index += 1
        line_count += 1
    print("Processed " + str(line_count) + " lines.")
    for x in range(3):
        print "Item " + str(x) + ": " + matrix[x][0] + ", " + matrix[x][1] + ", " + matrix[x][2]
    # print(matrix)
    # print(labels)