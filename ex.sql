SELECT 
  SessionId,
  ANY_VALUE(type) as type,
  ANY_VALUE(device) as device,
  ANY_VALUE(region) as region,
  SUM(page_count) as page_count,
  MIN(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as start_time,
  MAX(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as end_time
  FROM(
  
  SELECT
          date,
          SessionId,
          (CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) as type,
          (CASE WHEN ObjectType LIKE 'device' THEN ObjectId ELSE NULL END) as device,
          (CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) as region,
  --         subquery and join on date for the session, select date and get min and max for entire session ID        
          COUNT(CASE WHEN ObjectType LIKE 'page' THEN 1 ELSE NULL END) as page_count

      FROM usf_research.Informatica_Data_ALL_06012018_07312018
--       WHERE SessionId = '03IbtwFMb4z5Z62DItC3Vl'
--       WHERE ((CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) IS NOT NULL
--       OR (CASE WHEN ObjectType LIKE 'device' THEN ObjectId ELSE NULL END) IS NOT NULL
--       OR (CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) IS NOT NULL
--       OR (CASE WHEN ObjectType LIKE 'page' THEN ObjectId ELSE NULL END) IS NOT NULL)

      GROUP BY type, device, region, date, SessionId
--       LIMIT 12
  )
--     WHERE SessionId = '03IbtwFMb4z5Z62DItC3Vl'
--     WHERE page_count != 0
    GROUP BY SessionId
    ORDER BY SessionId
    LIMIT 10000
