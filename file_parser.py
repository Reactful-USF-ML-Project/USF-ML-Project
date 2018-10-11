import csv

with open('../Downloads/results-20181008-130002 - results-20181008-130002.csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    session_ids = []
    matrix = []
    # matrix_index = 0 
    for row in csv_reader:
        if line_count == 0:
            labels = [] 
            for l in row: 
                labels.append(l)
        else:
            sid = row[2]
            if sid in session_ids:
                continue
            else:
                matrix.append([])
                # session_ids.append(sid)
                # matrix_index += 1
        line_count += 1
    print("Processed " + str(line_count) + " lines.")
    # print(session_ids)
    print(matrix)