import csv
import numpy
from datetime import datetime

def update_dict(dictionary, object_key, object_value):
    if object_key not in dictionary:
        dictionary.update({object_key:[]})
        dictionary[object_key].append(object_value)
    elif object_value not in dictionary[object_key]:
        dictionary[object_key].append(object_value)

def timestamp_to_date(time):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_session_length(start, end):
    return int((end - start).total_seconds() * 1000000)

def store_to_current_session(key,value,current_session,possible_values,map_to_session_index):

    if key == "page":
        current_session[map_to_session_index['page_count']] += 1
    elif key == "reaction" or key == "goal" or key == "type" or key == "device" or key == "region":
        update_dict(possible_values, key, value)
        position_in_possibles = possible_values[key].index(value)
        # print('position_in_possibles: %d' % position_in_possibles)
        current_session[map_to_session_index[key]][position_in_possibles] = 1
    elif key in map_to_session_index:
        update_dict(possible_values, key, value)
        position_in_possibles = possible_values[key].index(value)
        current_session[map_to_session_index[key]] = position_in_possibles

# Ordering of a session so far (used in map_to_session_index):
# [ average time on page, region, type, device, page count, reaction combination, goal combination, session_length]
def get_matrix():
    with open('informatica_completed_reactions.csv') as csv_file:
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
                sid = row[0]

                if sid in session_ids: # We have seen this one before
                    current_session = matrix[matrix_index]

                    # Check to see if the time happens to be larger or smaller than the prior
                    time = timestamp_to_date(row[1])
                    if time < start_time:
                        start_time = time
                    elif time > end_time:
                        end_time = time

                    object_key = row[4]
                    object_value = row[5]
                    store_to_current_session(object_key,object_value,current_session,possible_values,map_to_session_index)

                else: # This is a new session so we need to do a few things
                    if matrix_index > 0:
                        last_session = matrix[matrix_index - 1]

                        # Update Reaction Sequence to be an integer than a string
                        # hashed_reaction_sequence = hash(last_session[map_to_session_index['reaction']])
                        # last_session[map_to_session_index['reaction']] = hashed_reaction_sequence
                        # update_dict(possible_values, 'reaction', hashed_reaction_sequence)

                        # Update Goal Sequence to be an integer than a string
                        # hashed_goal_sequence = hash(last_session[map_to_session_index['goal']])
                        # last_session[map_to_session_index['goal']] = hashed_goal_sequence
                        # update_dict(possible_values, 'reaction', hashed_goal_sequence)

                        # Need to calculate average time per page
                        session_length = get_session_length(start_time, end_time)
                        last_session[map_to_session_index['session_length']] = session_length
                        page_count = last_session[map_to_session_index['page_count']]

                        if session_length > 0 and page_count > 0:    
                            last_session[map_to_session_index['avg_time_per_page']] = session_length / page_count
                        else:
                            last_session[map_to_session_index['avg_time_per_page']] = 0

                    matrix_index += 1
                    session_ids.append(sid)

                    new_session = numpy.empty(len(map_to_session_index), dtype=object)
                    matrix.append(new_session)

                    # Check if time is smaller than min or greater than max
                    time = timestamp_to_date(row[1])
                    start_time = time
                    end_time = time

                    current_session = matrix[matrix_index]

                    # Set default values
                    current_session[map_to_session_index['reaction']] = [0] * 10 # 10 being the number of reactions seen
                    current_session[map_to_session_index['goal']] = [0] * 9
                    current_session[map_to_session_index['type']] = [0] * 2
                    current_session[map_to_session_index['device']] = [0] * 1
                    current_session[map_to_session_index['region']] = [0] * 229
                    current_session[map_to_session_index['page_count']] = 0 # Default page_count value of zero 
                    current_session[map_to_session_index['session_length']] = 0
                    current_session[map_to_session_index['avg_time_per_page']] = 0

                    # Need to store whatever is in this row
                    object_key = row[4]
                    object_value = row[5]
                    store_to_current_session(object_key,object_value,current_session,possible_values,map_to_session_index)
     
            line_count += 1
            
        print("Processed " + str(line_count) + " lines.")
        return (matrix, possible_values)

if __name__ == "__main__": #If running the file on it's own just run the get_matrix() routine and print it
    (matrix, possible_values) = get_matrix()
    for a in matrix:
        result = ", ".join(map(str, a))
        print result
    for possible_value in possible_values:
        print possible_value+": "+", ".join(map(str, possible_values[possible_value]))





