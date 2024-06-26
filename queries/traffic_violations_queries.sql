-- TRAFFIC VIOLATION QUERIES
-- WHICH MAKE AND MODEL INVOLVED IN MOST CRASHES
SELECT 
  make,model,
  COUNT(*) AS crash_count
FROM 
  umd-inst767.montgomery_datasets.traffic_violations
WHERE 
  date_of_stop BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  make,model
ORDER BY 
  crash_count DESC
LIMIT 
  10;

-- MOST VIOLATIONS BASED ON LOCATION
SELECT 
  location,driver_state,
  COUNT(*) AS violation_count
FROM 
  umd-inst767.montgomery_datasets.traffic_violations
WHERE date_of_stop BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  location,driver_state
ORDER BY 
  violation_count DESC;

-- MOST COMMON VIOLATIONS IN 2023
SELECT 
  description,
  COUNT(*) AS violation_count
FROM 
  umd-inst767.montgomery_datasets.traffic_violations
WHERE date_of_stop BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  description
ORDER BY 
  violation_count DESC
LIMIT 
  10;

-- NUMBER OF VIOLATED BASED ON GENDER, RACE AND ALCOHOL
SELECT 
  gender,
  race,
  alcohol,
  COUNT(*) AS violation_count
FROM 
  umd-inst767.montgomery_datasets.traffic_violations
WHERE date_of_stop BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  alcohol, gender, race
ORDER BY 
  violation_count DESC
;
