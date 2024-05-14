-- SQL Query created by Yasmin
-- description:
-- this query joins the crimes table and the crashes table using right join
-- then we count the number of crime by street name and crime name
-- only crime from 2023 is kept

-- starting with crimes table then bringing in crashes table using right join
WITH latitude_longitude AS (
  SELECT 
      crimes.latitude, 
      crimes.longitude, 
      crimes.beat, 
      crimes.crimename1,
      crashes.cross_street_name,
      crashes.road_name,
      crashes.crash_date_time
  FROM 
      `umd-inst767.montgomery_datasets.crimes` AS crimes
  RIGHT JOIN 
      `umd-inst767.montgomery_datasets.crashes` AS crashes

-- casting latitude and longitude to reduce discrepancies due to floating points
  ON 
      ABS(CAST(crimes.latitude AS FLOAT64) - CAST(crashes.latitude AS FLOAT64)) < 0.0001 
      AND ABS(CAST(crimes.longitude AS FLOAT64) - CAST(crashes.longitude AS FLOAT64)) < 0.0001
)

-- selecting street name and crime name to create a count column
SELECT 
  cross_street_name, 
  crimename1,
  COUNT(crimename1) AS crime_count
FROM 
  latitude_longitude
WHERE 
  crimename1 IS NOT NULL -- removing rows with null values in crime name since we want crime types
  AND EXTRACT(YEAR FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%E*S', crash_date_time)) = 2023 -- filtered to include only year 2023
GROUP BY 
  cross_street_name, 
  crimename1
ORDER BY 
  cross_street_name, crimename1, crime_count DESC;
