-- CRIME API QUERIES
-- CRIME AGAINST PROPERTY IN SILVER SPRING IN 2022 to 2024 #
SELECT * FROM umd-inst767.montgomery_datasets.crimes
WHERE crimename1='Crime Against Person'
AND district = 'SILVER SPRING'
AND date BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY date ASC;


-- TOP 10 MOST COMMON OFFENCES
SELECT offence_code, crimename1, crimename2,
  crimename3, COUNT(*) AS offence_count 
FROM umd-inst767.montgomery_datasets.crimes 
WHERE crimename1 = 'Crime Against Person' AND start_date BETWEEN '2023-01-01' AND '2023-12-31' 
GROUP BY offence_code, crimename1, crimename2,crimename3
ORDER BY offence_count DESC 
LIMIT 10;

-- ADDRESS STREET WITH MOST OFFENCES
SELECT 
  address_street,city,
  COUNT(*) AS offence_count
FROM 
  umd-inst767.montgomery_datasets.crimes 
WHERE start_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  address_street ,city
ORDER BY 
  offence_count DESC 
LIMIT 
  10;

-- CITY WITH MOST OFFENCES 
SELECT 
  city,
  COUNT(*) AS offence_count
FROM 
  umd-inst767.montgomery_datasets.crimes 
WHERE start_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 
  city
ORDER BY 
  offence_count DESC
LIMIT 
  10;

-- CRIMES WITH MORE THAN 1 VICTIM INVOLVED
SELECT 
  incident_id,
  crimename1,
  city,
  COUNT(CAST(victims AS INT64)) AS victim_count
FROM 
  umd-inst767.montgomery_datasets.crimes
GROUP BY 
  incident_id, crimename1, city
HAVING 
  COUNT(CAST(victims AS INT64)) > 1
ORDER BY 
  victim_count DESC;
