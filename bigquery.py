import csv
import numpy
import os
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

# my editions
# https://www.blendo.co/blog/access-data-google-bigquery-python-r/
from google.cloud import bigquery
from google.oauth2 import service_account

def get_matrix():
  # credentials = service_account.Credentials.from_service_account_file('path/to/file.json')
  credentials = service_account.Credentials.from_service_account_file(
      os.environ['USF_ML_PROJECT'])
  project_id = 'usf-ml-project'

  client = bigquery.Client(credentials=credentials, project=project_id)

  query = ("""
  SELECT 
    ANY_VALUE(type) as type,
    ANY_VALUE(device) as device,
    ANY_VALUE(region) as region,
    STRING_AGG(reaction) as reaction,
    SUM(page_count) as page_count,
    MIN(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as start_time,
    MAX(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as end_time
  FROM(
    
    SELECT
      date,
      ALL_SESSION_FOR_CLIENT.SessionId as SessionId,
      (CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) as type,
      (CASE WHEN ObjectType LIKE 'device' THEN ObjectId ELSE NULL END) as device,
      (CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) as region,
      (CASE WHEN ObjectType LIKE 'reaction' THEN ObjectId ELSE NULL END) as reaction,
  --         subquery and join on date for the session, select date and get min and max for entire session ID        
      COUNT(CASE WHEN ObjectType LIKE 'page' THEN 1 ELSE NULL END) as page_count

        FROM (
        SELECT
          date,
          SessionId,
          ObjectType,
          ObjectId,
          SourceType,
          EventName
        FROM usf_research.Informatica_Data_ALL_06012018_07312018) AS ALL_SESSION_FOR_CLIENT
    --    Getting all reactions to JOIN upon
        INNER JOIN (
          SELECT SessionID 
          FROM usf_research.Informatica_Data_ALL_06012018_07312018

          WHERE ObjectType = 'reaction' AND EventName like 'completed%'
        ) AS GOAL_COMPLETED_SESSION
    --    JOINing on reactions which have a completed reaction in their field by their SessionId
        ON 
        ALL_SESSION_FOR_CLIENT.SessionId = GOAL_COMPLETED_SESSION.SessionId

        GROUP BY ALL_SESSION_FOR_CLIENT.SessionId,  ALL_SESSION_FOR_CLIENT.date, ALL_SESSION_FOR_CLIENT.EventName, ALL_SESSION_FOR_CLIENT.ObjectType, ALL_SESSION_FOR_CLIENT.ObjectId, ALL_SESSION_FOR_CLIENT.SourceType
    )
      GROUP BY SessionId
      ORDER BY SessionId
          """)

  query_job = client.query(query)

  results = query_job.result()  # waits for job to complete

  # Ordering of a session so far (used in map_to_feature_name):
  # [ average time on page, region, type, device, page count, reaction combination, goal combination, session_length]
  # def get_matrix():

  # return (features, possible_values, completed_reactions)

  features = {
              'avg_time_per_page':[], 
              'region': [], #
              'type': [], #
              'device':  [], #
              'page_count': [], #
              'reaction': [],
              'goal': [],
              'session_length': [],
          }
  labels = []
  possible_values = {
    'avg_time_per_page':[], 
    'region': [], #
    'type': [], #
    'device':  [], #
    'page_count': [], #
    'reaction': [],
    'goal': [],
    'session_length': [],
  }

  for result in results:
      features['region'].append(result['region'])
      update_dict(possible_values,'region',result['region'])
      features['type'].append(result['type'])
      update_dict(possible_values,'type',result['type'])
      features['device'].append(result['device'])
      update_dict(possible_values,'device',result['device'])
      features['page_count'].append(result['page_count'])
      update_dict(possible_values,'page_count',result['page_count'])

      # split up reaction that we aggregated on ','
      reactions = result['reaction'].split(',')
      features['reaction'].append(reactions)
      for reaction in reactions:
        update_dict(possible_values,'reaction',reaction)


      label = reactions[-1]
      labels.append(label)
      session_length = result['end_time'] - result['start_time']
      avg_time_per_page = (session_length)/result["page_count"]
      features['session_length'].append(session_length)
      features['avg_time_per_page'].append(avg_time_per_page)


      print("Pulled all data down from BigQuery...")
  return (features, possible_values, labels)
  # if __name__ == "__main__":  # If running the file on it's own just run the get_matrix() routine and print it
  #     # Start from here
      # print(results.to_dataframe())
