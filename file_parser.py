import csv
import numpy
from datetime import datetime

""" Updates the dictionary containing the object key and object
    value key value pair. If the object key is not in the 
    dictionary, the key is added to the dictionary with an empty
    array as the value. The object value is then added to the 
    empty array. Otherwise, the object value is appended to the
    existing array. 

    Arguments:
     - dictionary: 
            dictionary to be updated 
     - object_key:
            key to be either searched in or added to dictionary
     - object_value: 
            value to be either searched in or added to dictionary
"""
def update_dict(dictionary, object_key, object_value):
    if object_key not in dictionary:
        dictionary.update({object_key:[]})
        dictionary[object_key].append(object_value)
    elif object_value not in dictionary[object_key]:
        dictionary[object_key].append(object_value)


""" Takes in a timestamp as a string and converts it to a 
    datetime according to the given format. 

    Arguments:
     - time: 
            timestamp as a string

    Return:
     - timestamp string as a datetime
"""
def timestamp_to_date(time):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")


""" Gets the length of a session. 

    Arguments:
     - start: 
            start time of session
     - end: 
            end time of session

    Return: 
     - length of session
"""
def get_session_length(start, end):
    return int((end - start).total_seconds() * 1000000)


""" 
"""
def store_to_current_session(key,value,features,possible_values,map_to_feature_name):

    if key == "page":
        features[map_to_feature_name['page_count']][-1] += 1
    # elif key == "reaction" or key == "goal":
    #     update_dict(possible_values, key, value)
    #     position_in_possibles = possible_values[key].index(value)
    #     # print('position_in_possibles: %d' % position_in_possibles)
    #     current_session[map_to_feature_name[key]].append(value)
    elif key in map_to_feature_name:
        update_dict(possible_values, key, value)
        # position_in_possibles = possible_values[key].index(value)
        if value not in features[map_to_feature_name[key]][-1]:
            features[map_to_feature_name[key]][-1].append(value)

# Ordering of a session so far (used in map_to_feature_name):
# [ average time on page, region, type, device, page count, reaction combination, goal combination, session_length]
def get_matrix():
    with open('informatica_completed_reactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        session_ids = []
        features = {
            'avg_time_per_page':[],
            'region': [],
            'type': [],
            'device':  [],
            'page_count': [],
            'reaction': [],
            'goal': [],
            'session_length': []
        }
        matrix_index = -1
        start_time = -1
        end_time = -1
        possible_values = {}
        map_to_feature_name = {
            'avg_time_per_page': 'avg_time_per_page',
            'region': 'region',
            'type': 'type',
            'device':  'device',
            'page_count': 'page_count',
            'reaction': 'reaction',
            'goal': 'goal',
            'session_length': 'session_length'
        }
        completed_reactions = []
        for row in csv_reader:
            if line_count == 0:
                labels = [] 
                for l in row: 
                    labels.append(l)
            else:
                sid = row[0]

                if sid in session_ids: # We have seen this one before

                    # Check to see if the time happens to be larger or smaller than the prior
                    time = timestamp_to_date(row[1])
                    if time < start_time:
                        start_time = time
                    elif time > end_time:
                        end_time = time

                    object_key = row[4]
                    object_value = row[5]
                    if object_key == "reaction":
                        if matrix_index >= len(completed_reactions):
                            completed_reactions.append(object_value)
                        else:
                            completed_reactions[matrix_index] = object_value
                    store_to_current_session(object_key,object_value,features,possible_values,map_to_feature_name)

                else: # This is a new session so we need to do a few things
                    if matrix_index > 0:

                        # Update Reaction Sequence to be an integer than a string
                        # hashed_reaction_sequence = hash(last_session[map_to_feature_name['reaction']])
                        # last_session[map_to_feature_name['reaction']] = hashed_reaction_sequence
                        # update_dict(possible_values, 'reaction', hashed_reaction_sequence)

                        # Update Goal Sequence to be an integer than a string
                        # hashed_goal_sequence = hash(last_session[map_to_feature_name['goal']])
                        # last_session[map_to_feature_name['goal']] = hashed_goal_sequence
                        # update_dict(possible_values, 'reaction', hashed_goal_sequence)

                        # Need to calculate average time per page
                        session_length = get_session_length(start_time, end_time)
                        features[map_to_feature_name['session_length']][-1] = session_length
                        page_count = features[map_to_feature_name['page_count']][-1]

                        if session_length > 0 and page_count > 0:    
                            features[map_to_feature_name['avg_time_per_page']][-1] = session_length / page_count
                        else:
                            features[map_to_feature_name['avg_time_per_page']][-1] = 0

                    matrix_index += 1
                    session_ids.append(sid)

                    # Check if time is smaller than min or greater than max
                    time = timestamp_to_date(row[1])
                    start_time = time
                    end_time = time

                    # Set default values
                    features[map_to_feature_name['reaction']].append([]) # 10 being the number of reactions seen
                    features[map_to_feature_name['goal']].append([])
                    features[map_to_feature_name['type']].append([])
                    features[map_to_feature_name['device']].append([])
                    features[map_to_feature_name['region']].append([])
                    features[map_to_feature_name['page_count']].append(0) # Default page_count value of zero 
                    features[map_to_feature_name['session_length']].append(0)
                    features[map_to_feature_name['avg_time_per_page']].append(0)

                    # Need to store whatever is in this row
                    object_key = row[4]
                    object_value = row[5]
                    if object_key == "reaction":
                        if matrix_index >= len(completed_reactions):
                            completed_reactions.append(object_value)
                        else:
                            completed_reactions[matrix_index] = object_value
                    store_to_current_session(object_key,object_value,features,possible_values,map_to_feature_name)
     
            line_count += 1
            
        print("Processed " + str(line_count) + " lines.")
        return (features, possible_values, completed_reactions)


if __name__ == "__main__": #If running the file on it's own just run the get_matrix() routine and print it
    (features, possible_values, completed_reactions) = get_matrix()
    for feature in features:
        print(feature+": "+", ".join(map(str, features[feature])))
    for possible_value in possible_values:
        print(possible_value+": "+", ".join(map(str, possible_values[possible_value])))


    # for rid in completed_reactions:
    #     print str(rid) + "\n"

    print("Matrix len: " + str(len(features['page_count'])))
    print("Reaction list len: " + str(len(completed_reactions)))





