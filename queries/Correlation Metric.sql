with traffic_violations as (
  select round(cast(a.latitude as FLOAT64), 2) as latitude
      , round(cast(a.longitude as FLOAT64), 2) as longitude
      , count(concat(latitude, longitude, date_of_stop)) as violations
  from montgomery_datasets.traffic_violations a
  where date(date_of_stop) between date('2023-01-01') and date('2023-12-31')
  group by 1,2
),

crashes as (
  select round(cast(b.latitude as FLOAT64), 2) as latitude
    , round(cast(b.longitude as FLOAT64), 2) as longitude
    , count(concat(latitude, longitude, crash_date_time)) as crashes
  from montgomery_datasets.crashes b
  where date(crash_date_time) between date('2023-01-01') and date('2023-12-31')
  group by 1,2
),

crimes as (
  select round(cast(c.latitude as FLOAT64), 2) as latitude
    , round(cast(c.longitude as FLOAT64), 2) as longitude
    , count(concat(latitude, longitude, date)) as crimes
  from montgomery_datasets.crimes c
  where date(start_date) between date('2023-01-01') and date('2023-12-31')
  and date is not null
  group by 1,2 
)

select round(corr(crashes, violations)*100,2) as corr_violations_crashes
  , round(corr(crashes, crimes)*100,2) as corr_crashes_crimes
  , round(corr(violations, crimes)*100,2) as corr_violations_crimes
from traffic_violations tv
join crashes cr on tv.latitude = cr.latitude and tv.longitude = cr.longitude
join crimes c on tv.latitude = c.latitude and tv.longitude = c.longitude;