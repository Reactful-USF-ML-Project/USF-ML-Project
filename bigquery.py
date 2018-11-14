import csv
import numpy
from datetime import datetime

# my editions
# https://www.blendo.co/blog/access-data-google-bigquery-python-r/
from google.cloud import bigquery
from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file('path/to/file.json')
credentials = service_account.Credentials.from_service_account_file(
    '/Users/johnmurray/Downloads/USF-ML-Project-9792f2f97e42.json')
project_id = 'usf-ml-project'

client = bigquery.Client(credentials = credentials, project = project_id)

basequery = ("""

    SELECT
        ALL_SESSION_FOR_CLIENT.SessionId,
        ALL_SESSION_FOR_CLIENT.date,
        ALL_SESSION_FOR_CLIENT.EventName,
        ALL_SESSION_FOR_CLIENT.SourceType,
        ALL_SESSION_FOR_CLIENT.ObjectType,
        ALL_SESSION_FOR_CLIENT.ObjectId
        FROM (
        SELECT
        date,
        SessionId,
        ObjectType,
        ObjectId,
        SourceType,
        EventName
        FROM usf_research.Informatica_Data_ALL_06012018_07312018
        ) AS ALL_SESSION_FOR_CLIENT

        INNER JOIN (
        SELECT SessionID 
        FROM usf_research.Informatica_Data_ALL_06012018_07312018

        WHERE ObjectType = 'reaction' AND EventName like 'completed%'

        ) AS GOAL_COMPLETED_SESSION

        ON 
        ALL_SESSION_FOR_CLIENT.SessionId = GOAL_COMPLETED_SESSION.SessionId

        GROUP BY ALL_SESSION_FOR_CLIENT.SessionId,  ALL_SESSION_FOR_CLIENT.date, ALL_SESSION_FOR_CLIENT.EventName, ALL_SESSION_FOR_CLIENT.ObjectType, ALL_SESSION_FOR_CLIENT.ObjectId, ALL_SESSION_FOR_CLIENT.SourceType

        ORDER BY  ALL_SESSION_FOR_CLIENT.SessionID
        """)

query_job = client.query("""

    SELECT
--         date,
        SessionId,
--         ObjectType,
--         ObjectId,
--         SourceType,
--         EventName,
        (CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) as type,
        (CASE WHEN ObjectType LIKe 'device' THEN ObjectId ELSE NULL END) as device,
        (CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) as region,
--         subquery and join on date for the session, select date and get min and max for entire session ID
--         
        MIN(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as start_time,
        MAX(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as end_time
      
    FROM usf_research.Informatica_Data_ALL_06012018_07312018
    WHERE SessionId = '03IbtwFMb4z5Z62DItC3Vl'
    AND ((CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) IS NOT NULL
    OR (CASE WHEN ObjectType LIKE 'device' THEN ObjectId ELSE NULL END) IS NOT NULL
    OR (CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) IS NOT NULL)
    
    GROUP BY SessionID, date, type, device, region





        #LIMIT 1000""", job_config=job_config)

results = query_job.result() # waits for job to complete

# Ordering of a session so far (used in map_to_feature_name):
# [ average time on page, region, type, device, page count, reaction combination, goal combination, session_length]
# def get_matrix():
    
        # return (features, possible_values, completed_reactions)


if __name__ == "__main__": #If running the file on it's own just run the get_matrix() routine and print it
    # Start from here
    print(results.to_dataframe())






