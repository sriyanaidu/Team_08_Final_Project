# Big Data Final Project
INST 767: Big Data Infrastructure  
Professor: Zach Drake

## Team Members
Aryaman Paigankar

Goutham Patchipulusu

Sai Satya Sriya Naidu Kola

Sakshi Patil

Tanya Gupta

N. Yasmin Bromir

# Analyzing Crime, Crash Reporting, and Traffic Violations
With a focus on Montgomery County in Maryland, we will be analyzing data about crimes, crashes, and traffic violations to establish if there are any relationships between crimes, crashes, and locations.

# Background
Our project is centered around leveraging datasets provided by Montgomery County’s open data website, [data.Montgomery](https://data.montgomerycountymd.gov/). This platform offers access to various datasets, including crime statistics databases, crash data, and information on traffic violations. By utilizing these datasets, we aim to provide the public with valuable insights into crime trends, traffic patterns, and safety issues within Montgomery County. Through data analysis and visualization, we seek to empower stakeholders (local residents) with the information they need to make informed decisions and improve grassroots community safety initiatives.

## Business Problem
Montgomery County residents can enhance public safety awareness and reduce traffic-related incidents through the effective utilization of available data sources, including crime data, crash reporting incidents data, and traffic violations data. However, the current lack of comprehensive data analysis and integration presents challenges in identifying high-risk areas, understanding contributing factors, and implementing proactive interventions.

Key goals for our analysis and visualizations include identifying high-traffic violation areas, understanding historical crimes, and mapping the frequency of crashes. Residents can then use this knowledge to implement targeted interventions aimed at promoting traffic safety and reducing violations, as well as making sure that community resources are being properly allocated.

Expected outcomes include improved awareness of local crimes, understanding of traffic safety issues, and more informed grassroots advocacy by stakeholders. By educating themselves about local traffic violations and other crime, the residents of Mongtomery County can take proactive measures to address safety concerns, promote safer road behavior, and make sure that county resources are being properly allocated.

**Business Questions**

The following business questions guided our SQL queries and visualizations. We focused on questions that would have some real-world applications by improving the presence of police, showcasing correlations between events, and breaking down previous crime to predict future crime.


1. Are there correlations between crimes, crashes, and traffic violations in the places they occur? If so, what is the strength of the correlation?
   1. The crashes and crimes happening in a area have a good correlation of 71.34% and then the traffic violations and the crashes have a correaltion of 61.47% and finally the violations and crimes have a 51% correlation.
2. What is the connection between crimes, crashes, and weather?
   1. Most number of crashes occur on clear days, followed by rainy days and then cloudy days. 
3. Historically, what types of crimes and crashes have previously occured on each street?
   1. If we take a look at the latitude_longitude.sql query, the API data from crashes and crime is joined into one table and then filtered out by year (only 2023), and then grouped by street name and crime name. We can see that some streets list 'Crime Against Person', 'Crime Against Property', and 'Crime Against Society' while others list only one or two of these types of crimes. For futher analysis, a visualization could be created from this query, including some geospatial analysis by using the latitude and longitude.
4. What are the common causes of traffic crashes, and how do they vary by light conditions and intersection types?
   1. Answered in the analysis
5. What are the most common types of crimes committed in different areas, and how are they distributed geographically?
   1. Answered in the analysis
6. How do traffic violation trends change over time, and what might be influencing these trends?
   1. Answered in the analysis

## Project Description
Using open source data sources from Montgomery County, we pulled information from three APIs: crimes, crashes, and traffic violations. Then we transformed the data from the three APIs to perform analysis for our business questions. 

See DAG below: 

![Data_Architecture](https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/5e756fb0-3f0f-4d43-87bd-695d67992985)

# Application Architecture 

The DAG above provides a general view on our processes. The following sections provide further details on how the data was retrieved, cleaned, and made usable for our SQL queries and visualizations.

## Ingest

### About the APIs from Montgomery County

**Crime Data**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/icn6-v9z3)

This API provides daily postings from Montgomery County's open data website which provides the public with direct access to crime statistic databases. The data provided comes from "EJustice", which is a records-management system used by Montgomery County Police Department.

Limitations of the data: Information may not be verified due to investigations, and classifications may be changed in the future.

**Crash Reporting - Incidents Data**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/bhju-22kf)

This API provides general information about each collision and details of all traffic collisions occurring on county and local roadways in Montgomery County. Data incorporates information from the Automated Crash Reporting System (ACRS), as well as information from Montgomery County Police, Gaithersburg Police, Rockville Police, and the Maryland-National Capital Park Police.

Limitations of the data: Information is based on preliminary reporting and may not be verified, data may change at a later date after further investigation.

Updated: Weekly

**Traffic Violations**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/4mse-ku6q)

This API contains information about traffic violations from all electronic traffic violations issued within Montgomery County.

Limitations of the data: any information that can be used to uniquely identify the vehicle, vehicle owner, or the office issuing the violation is not published.

Updated: Daily

### Cloud Functions
<img width="1416" alt="Cloud Functions" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/d81dfc1f-6e63-42bf-b03f-be084548ae7d">

Within Google Cloud Platform, we used the Python-based Cloud Functions to facilitate the execution of APIs for data collection. These codes utilize the login credentials and the API token to access the API and collect the data. Following data collection, the Cloud Function transfers the gathered data into the corresponding storage buckets before further processing takes place.

### Storage Buckets
<img width="1416" alt="Storgae Buckets" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/b34cc178-5635-4f11-992e-b6e01d974701">

After using Cloud Functions, we move on to the storage of the data. Within Cloud Storage we implemented a data management system by creating separate buckets for each data source: crashes, crime, and traffic violations. These buckets, named "crashesumd", "crime_bucket_api", and "inst767trafficviolationsbucket", respectively, were designed to organize and store the data collected from the corresponding APIs. Though the data is fairly structured, each API presents different data, and using Cloud Storage allowed us to properly handle such data.

The layout for each bucket looks similar to this:

<img width="1416" alt="Screenshot 2024-05-15 at 1 44 06 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/8778e175-b3b1-4fbb-a54f-3456029cc9c2">

### Cloud Scheduler
<img width="1416" alt="Cloud Scheduler" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/630825c5-8bca-4983-a9fe-e6be70f20a7f">

The Cloud Scheduler is a cron job service that is implemented to automate data updates everyday at 9 AM EDT, ensuring that every time the scheduler runs for each API call, the relevant folder within the respective bucket is automatically updated with the latest data.

## Transform

We stored the Spark jobs code in our Cloud Storage bucket called `pyspark_bucket_inst767`. Each PySpark file transforms the data stored in the Cloud Storage buckets and then pushes them to the BigQuery tables.

Its layout looks like this: 

<img width="1416" alt="Buckets" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160181412/68014c35-c8be-4185-83e0-24269677e14b">

Each Pyspark file performs the following processes on our datasets:

- **Data Cleaning**:
  - Removed specified columns that are not relevant to the analysis, such as computed regions, agency-related information, geolocation data, etc.
  - Cleaned inconsistent values in certain columns by replacing "unknown" values with null and "N/A" values with empty strings.
  - Handled missing values in multiple columns by dropping rows with missing data or filling them with appropriate values.
  - Cleaned latitude and longitude columns by filtering out zero values and nulls.

- **Data Transformation**:
  - Loaded each dataset into a data frame using PySpark code.
  - Applied cleaning functions to handle missing and inconsistent values across all datasets.
  - Removed unnecessary columns to focus on relevant data for analysis.
  - Converted latitude and longitude columns to float type for numerical analysis.

- **Pushing Data to BigQuery**:
  - The cleaned DataFrames were written to BigQuery tables in the `montgomery_datasets` dataset.
  - The write operation for each dataset was performed using the `write` method of the DataFrame, specifying the respective BigQuery table names (`traffic_violations`, `crashes`, `crimes`) and the temporary GCS bucket for data transfer.
  - The mode was set to "overwrite" to replace any existing data in the destination tables. This ensures that the BigQuery tables are updated with the latest cleaned data, maintaining data consistency and accuracy for subsequent analysis. Additionally, duplicate records are automatically removed during the overwrite process, preventing redundant data in the tables.

<img width="1439" alt="BigQuery tables" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160181412/a6e45a08-d4c5-4d06-a560-8b1e2f371922">

Additionally, workflows have been created using the Dataproc through which a temporary cluster and a job is created to process the data and push to the final BigQuery tables. The workflows are set to run everyday with the help of Cloud Scheduler. Each Cloud Scheduler is set to trigger everyday at a particular time period:

- Traffic data workflow : Everyday 10am EDT
- Crimes data workflow : Everyday at 11am EDT
- Crashes data workflow : Everyday 12:30pm EDT

**Workflows**
<img width="1416" alt="Screenshot 2024-05-15 at 2 45 30 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/98a15f06-a9c0-4e64-917b-2f19f74ba1fa">

**Jobs**
<img width="1416" alt="Screenshot 2024-05-15 at 2 50 15 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/b1ba5f58-682c-4b83-8554-277a8fd8320d">

## Storage
For our storage solution, we opted to utilize BigQuery for its capabilities and compatibility with our project requirements. In addition to storing our data in BigQuery, we structured the storage by creating a database called Montgomery Datasets and in that we created separate tables for each API: crashes, crimes, and traffic violations.

### Crimes Dataset Schema

| Name                   | Type       |
|------------------------|------------|
| address_number         | STRING     |
| address_street         | STRING     |
| agency                 | STRING     |
| beat                   | STRING     |
| case_number            | STRING     |
| city                   | STRING     |
| crimename1             | STRING     |
| crimename2             | STRING     |
| crimename3             | STRING     |
| date                   | TIMESTAMP  |
| district               | STRING     |
| incident_id            | STRING     |
| latitude               | FLOAT      |
| location               | STRING     |
| longitude              | FLOAT      |
| nibrs_code             | STRING     |
| offence_code           | STRING     |
| place                  | STRING     |
| police_district_number | STRING     |
| pra                    | STRING     |
| sector                 | STRING     |
| start_date             | TIMESTAMP  |
| state                  | STRING     |
| street_type            | STRING     |
| victims                | INTEGER    |
| zip_code               | STRING     |

### Crashes Dataset Schema

| Name                     | Type       |
|--------------------------|------------|
| acrs_report_type         | STRING     |
| agency_name              | STRING     |
| at_fault                 | BOOLEAN    |
| collision_type           | STRING     |
| crash_date_time          | TIMESTAMP  |
| driver_substance_abuse   | STRING     |
| first_harmful_event      | STRING     |
| fixed_object_struck      | STRING     |
| hit_run                  | BOOLEAN    |
| lane_number              | INTEGER    |
| latitude                 | FLOAT      |
| light                    | STRING     |
| local_case_number        | STRING     |
| longitude                | FLOAT      |
| nontraffic               | BOOLEAN    |
| number_of_lanes          | INTEGER    |
| report_number            | STRING     |
| second_harmful_event     | STRING     |
| traffic_control          | STRING     |
| weather                  | STRING     |
| cross_street_name        | STRING     |
| cross_street_type        | STRING     |
| direction                | STRING     |
| distance                 | FLOAT      |
| distance_unit            | STRING     |
| intersection_area        | STRING     |
| intersection_type        | STRING     |
| junction                 | STRING     |
| lane_direction           | STRING     |
| mile_point               | FLOAT      |
| mile_point_direction     | STRING     |
| municipality             | STRING     |
| road_alignment           | STRING     |
| road_condition           | STRING     |
| road_division            | STRING     |
| road_grade               | STRING     |
| road_name                | STRING     |
| route_type               | STRING     |
| surface_condition        | STRING     |

### Traffic Violations Dataset Schema

| Name                     | Type       | Mode     |
|--------------------------|------------|----------|
| accident                 | STRING     | NULLABLE |
| alcohol                  | STRING     | NULLABLE |
| arrest_type              | STRING     | NULLABLE |
| article                  | STRING     | NULLABLE |
| belts                    | STRING     | NULLABLE |
| charge                   | STRING     | NULLABLE |
| color                    | STRING     | NULLABLE |
| commercial_license       | STRING     | NULLABLE |
| commercial_vehicle       | STRING     | NULLABLE |
| contributed_to_accident  | STRING     | NULLABLE |
| date_of_stop             | TIMESTAMP  | NULLABLE |
| description              | STRING     | NULLABLE |
| dl_state                 | STRING     | NULLABLE |
| driver_city              | STRING     | NULLABLE |
| driver_state             | STRING     | NULLABLE |
| fatal                    | STRING     | NULLABLE |
| gender                   | STRING     | NULLABLE |
| latitude                 | FLOAT      | NULLABLE |
| location                 | STRING     | NULLABLE |
| longitude                | FLOAT      | NULLABLE |
| make                     | STRING     | NULLABLE |
| model                    | STRING     | NULLABLE |
| personal_injury          | STRING     | NULLABLE |
| property_damage          | STRING     | NULLABLE |
| race                     | STRING     | NULLABLE |
| state                    | STRING     | NULLABLE |
| subagency                | STRING     | NULLABLE |
| time_of_stop             | TIME       | NULLABLE |
| vehicle_type             | STRING     | NULLABLE |
| violation_type           | STRING     | NULLABLE |
| work_zone                | STRING     | NULLABLE |
| year                     | INTEGER    | NULLABLE |


**Crashes Dataset**
<img width="1106" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/67585d3a-ef3d-49fc-9848-47e617802702">

**Crimes Dataset**
<img width="1110" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/84313030-0a19-460f-9533-80ecb84e66b2">

**Traffic_Violations Dataset**
<img width="1118" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/8ee2d1bb-05bd-4593-af94-525f82ea51a0">

## Analysis

In this project, we leveraged Looker Studio to analyze and visualize data across three key schemas: crashes, crimes, and traffic violations dataset, to derive actionable insights from complex information. Through a series of meaningful visualizations, such as trend analyses over time, geographical heatmaps, and distribution charts, we aim to illuminate patterns and trends that inform strategic decision-making. The dashboards created in Looker Studio not only highlights critical data points but also facilitates a deeper understanding of the underlying dynamics within each dataset.

**Crimes Dashboard**

The Crimes dashboard delves into the rate and distribution of crimes over time and across categories, utilizing a heat map to visualize geographical crime hotspots and identify regions requiring heightened security measures. Detailed pie charts and bar graphs break down crime types and locations, offering stakeholders a clear view of predominant crime patterns and enabling more effective community policing and resource allocation strategies.


![Screenshot 2024-05-15 163941](https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/2c04b5ea-5d0f-4098-a833-2a879981a0c0)




**Crashes Dashboard**

This dashboard explores traffic crashes, with visualizations that track crash occurrences over time and analyze them by light conditions, collision types, and intersection configurations. It provides critical insights into the conditions under which most crashes occur, such as time of day or specific traffic setups, aiding in the design of safer roads and more informed urban planning. The hit-and-run analysis further highlights the urgency of addressing driver accountability and enhancing surveillance measures.

![Screenshot 2024-05-15 164001](https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/eb64d759-2077-4e1e-80b9-5ad30d36d411)




**Traffic Violations Dashboard**

This dashboard presents a comprehensive analysis of traffic violations, categorized by gender, race, and case type to identify demographic patterns. A trend analysis chart provides insights into the fluctuation of violations over time, pinpointing potential seasonal or enforcement-related trends. Additionally, a geographic breakdown by city offers a detailed view of where most violations occur, assisting in targeted traffic enforcement and policy-making.


![Screenshot 2024-05-15 164019](https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/d66a67d8-7268-458a-bed9-7322d5eeac57)


[View the Looker Studio visualization report](https://lookerstudio.google.com/s/tY_R4xYcsF8)
