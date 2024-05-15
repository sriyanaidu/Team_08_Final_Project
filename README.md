# Big Data Final Project
INST 767: Big Data Infrastructure  
Professor: Zach Drake

## Team Members
Aryaman Paigankar

Goutham Patchipulusu

Sai Satya Sriya Naidu Kola

Sakshi Patil

Tanya Gupta

Yasmin Bromir

# Analyzing Crime, Crash Reporting, and Traffic Violations
With a focus on Montgomery County in Maryland, we will be analyzing data about crimes, crashes, and traffic violations to establish if there are any relationships between crimes, crashes, and locations.

# Background
Our project is centered around leveraging datasets provided by Montgomery County’s open data website, [data.Montgomery](https://data.montgomerycountymd.gov/). This platform offers access to various datasets, including crime statistics databases, crash data, and information on traffic violations. By utilizing these datasets, we aim to provide the public with valuable insights into crime trends, traffic patterns, and safety issues within Montgomery County. Through data analysis and visualization, we seek to empower stakeholders with the information they need to make informed decisions and improve community safety initiatives.

## Business Problem
The Montgomery County can enhance public safety and reduce traffic-related incidents through the effective utilization of available data sources, including crime data, crash reporting incidents data, and traffic violations data. However, the current lack of comprehensive data analysis and integration presents challenges in identifying high-risk areas, understanding contributing factors, and implementing proactive interventions.

Key goals include identifying high-traffic violation areas, understanding the crimes, crashes frequency, and understanding the factors contributing to violations. This knowledge can then be used to implement targeted educational initiatives and interventions aimed at promoting traffic safety and reducing violations.

Expected outcomes include improved awareness and understanding of traffic safety issues, enhanced educational programs, and more informed decision-making by stakeholders. By educating itself about traffic violations and their underlying causes, the county can take proactive measures to address safety concerns and promote safer road behavior.

## Project Description
Using open source data sources from Montgomery County, we pulled information from three APIs: crimes, crashes, and traffic violations. Then we transformed the data from the three APIs to perform analysis for our business questions. 

See DAG below: 

![Data_Architecture](https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/5e756fb0-3f0f-4d43-87bd-695d67992985)

# Application Architecture 

## Ingest

### APIs

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
<img width="1120" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/d81dfc1f-6e63-42bf-b03f-be084548ae7d">

The python based cloud functions have been developed to facilitate the execution of APIs for data collection via the Google Cloud Platform. These codes utilize the login credentials and the API token to access the API and collect the data. Following data collection, the cloud fucntions transfers the gathered data into the corresponding storage buckets before further process takes place.

### Storage Buckets
<img width="930" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/85833aa2-a1b9-47c7-89c5-2b1380002b60">

In Google Cloud Platform, we implemented a data management system by creating separate buckets for each data source: crashes, crime, and traffic violations. These buckets, named "crashesumd," "crime_bucket_api," and "inst767trafficviolationsbucket," respectively, were designed to organize and store the data collected from the corresponding APIs. Moreover, we implemented a scheduler to automate data updates everyday at 9 AM EDT, ensuring that each time the scheduler runs for each API call, the relevant folder within the respective bucket is automatically updated with the latest data.

### Cloud Scheduler
<img width="1116" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/b34b7247-380c-44e4-a370-6045917c120e">

The Cloud Scheduler is a cron job service which is used to run the cloud functions everyday at 9am EDT (0 9 * * *). The data is stored in their respective buckets as mentioned earlier.

## Transform

We stored the Spark jobs code in our code storage bucket called `pyspark_bucket_inst767`. Its layout looks like this: 

<img width="1436" alt="Buckets" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160181412/68014c35-c8be-4185-83e0-24269677e14b">


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
For our storage solution, we opted to utilize BigQuery for its capabilities and compatibility with our project requirements. In addition to storing our data in BigQuery, we structured the storage by creating a database called Montgomery Datasets and in that we created separate tables for each API: crashes, crimes, and traffic violations

**Crashes Dataset**
<img width="1106" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/67585d3a-ef3d-49fc-9848-47e617802702">

**Crimes Dataset**
<img width="1110" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/84313030-0a19-460f-9533-80ecb84e66b2">

**Traffic_Violations Dataset**
<img width="1118" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/8ee2d1bb-05bd-4593-af94-525f82ea51a0">

## Analysis

**Business Questions**
