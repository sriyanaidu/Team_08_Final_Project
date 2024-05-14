# number of count of accidents based on date and street address
SELECT 
    DATE_FORMAT(cr.crash_date_time, '%Y-%m-%d') AS crash_date,
    cr.address_street,
    COUNT(*) AS num_crashes
FROM 
    montgomery_datasets.crashes AS cr
GROUP BY 
    crash_date, cr.address_street
ORDER BY 
    crash_date, cr.address_street;


# count of number of crashes
SELECT 
    cr.cross_street_name,
    cr.first_harmful_event,
    cr.acrs_report_type,
    cr.collision_type,
    COUNT(*) AS num_crashes
FROM 
    montgomery_datasets.crashes AS cr
GROUP BY 
    cr.cross_street_name, cr.first_harmful_event, cr.acrs_report_type, cr.collision_type
ORDER BY 
    num_crashes DESC;



# number of crashes in each weather condition
SELECT 
    weather,
    COUNT(*) AS num_crashes
FROM 
    montgomery_datasets.crashes
GROUP BY 
    weather
ORDER BY 
    num_crashes DESC;
