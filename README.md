# Big Data Final Project
INST 767: Big Data Infrastructure  
Professor: Zach Drake

## Team Members
Sai Satya Sriya Naidu Kola

Goutham Patchipulusu

Sakshi Patil

Aryaman Paigankar

Tanya Gupta

N. Yasmin Bromir

# Analyzing Crime, Crash Reporting, and Traffic Violations
With a focus on Montgomery County in Maryland, we will be analyzing data about crimes, crashes, and traffic violations to establish if there are any correlations between events.

# Background
Our project leverages datasets provided by Montgomery County’s open data website, dataMontgomery, to provide the public with access to various crime statistic databases, crash data, and traffic violation information. 
## Business Problem
The Montgomery County can enhance public safety and reduce traffic-related incidents through the effective utilization of available data sources, including crime data, crash reporting incidents data, and traffic violations data. However, the current lack of comprehensive data analysis and integration presents challenges in identifying high-risk areas, understanding contributing factors, and implementing proactive interventions. By developing a data-driven approach, the county aims to analyze patterns and trends, forecast future risks, and collaborate with stakeholders to implement targeted interventions and improve overall public safety and traffic management in the area.
## Project Description

# Application Architecture 

## Ingest

**Crime Data**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/icn6-v9z3)

This API provides daily postings from Montgomery County's open data website which provides the public with direct access to crime statistic databases. The data provided comes from "EJustice", which is a records-management system used by Montgomery County Police Department.

Limitations of the data: information may not be verified due to investigations, and classifications may be changed in the future.

**Crash Reporting - Incidents Data**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/bhju-22kf)

This API provides general information about each collision and details of all traffic collisions occurring on county and local roadways in Montgomery County. Data incorporates information from the Automated Crash Reporting System (ACRS), as well as information from Montgomery County Police, Gaithersburg Police, Rockville Police, and the Maryland-National Capital Park Police.

Limitations of the data: information is based on preliminary reporting and may not be verified, data may change at a later date after further investigation.

Updated: Weekly

**Traffic Violations**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/4mse-ku6q)

This API contains information about traffic violations from all electronic traffic violations issued within Montgomery County.

Limitations of the data: any information that can be used to uniquely identify the vehicle, vehicle owner, or the office issuing the violation is not published.

Updated: Daily

-We implemented a data management system by creating separate buckets for each data source: crashes, crime, and traffic violations. These buckets, named "crashesumd," "crime_bucket_api," and "inst767trafficviolationsbucket," respectively, were designed to organize and store the data collected from the corresponding APIs. Moreover, we implemented a scheduler to automate data updates everyday 9 AM EDT, ensuring that each time the scheduler runs for each API call, the relevant folder within the respective bucket is automatically updated with the latest data.

<img width="1120" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/d81dfc1f-6e63-42bf-b03f-be084548ae7d">
Cloud Functions

<img width="930" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/9eef00d2-b524-461b-b7cf-98f290bf50ee">
     List of buckets created

<img width="1116" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/b34b7247-380c-44e4-a370-6045917c120e">
Cloud Scheduler

## Transform

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

<img width="1439" alt="big query tables" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160181412/a6e45a08-d4c5-4d06-a560-8b1e2f371922">

## Storage
For our storage solution, we opted to utilize BigQuery for its capabilities and compatibility with our project requirements. In addition to storing our data in BigQuery, we structured the storage by creating a database called Montgomery Datasets and in that we created separate tables for each api: crashes, crimes, and traffic violations

<img width="1106" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/67585d3a-ef3d-49fc-9848-47e617802702">
Crashes
<img width="1110" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/84313030-0a19-460f-9533-80ecb84e66b2">
Crimes
<img width="1118" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/8ee2d1bb-05bd-4593-af94-525f82ea51a0">
Treffic_Violations



## Analysis

## Management
