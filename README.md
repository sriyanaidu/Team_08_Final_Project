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
<img width="1416" alt="Cloud Functions" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/d81dfc1f-6e63-42bf-b03f-be084548ae7d">

The python based cloud functions have been developed to facilitate the execution of APIs for data collection via the Google Cloud Platform. These codes utilize the login credentials and the API token to access the API and collect the data. Following data collection, the cloud fucntions transfers the gathered data into the corresponding storage buckets before further process takes place.

### Storage Buckets
<img width="1416" alt="Storgae Buckets" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/b34cc178-5635-4f11-992e-b6e01d974701">

In Google Cloud Platform, we implemented a data management system by creating separate buckets for each data source: crashes, crime, and traffic violations. These buckets, named "crashesumd", "crime_bucket_api", and "inst767trafficviolationsbucket" respectively, were designed to organize and store the data collected from the corresponding APIs.

The layout for each bucket looks similar to this:

<img width="1416" alt="Screenshot 2024-05-15 at 1 44 06 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/8778e175-b3b1-4fbb-a54f-3456029cc9c2">

### Cloud Scheduler
<img width="1416" alt="Cloud Scheduler" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/630825c5-8bca-4983-a9fe-e6be70f20a7f">

The Cloud Scheduler is a cron job service is implemented to automate data updates everyday at 9 AM EDT, ensuring that each time the scheduler runs for each API call, the relevant folder within the respective bucket is automatically updated with the latest data.

## Transform

We stored the Spark jobs code in our code storage bucket called `pyspark_bucket_inst767`. In summary, each Pyspark file is written to transform the data which we have stored in the storage buckets and then push them to the big query tables.

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

<img width="1439" alt="big query tables" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160181412/a6e45a08-d4c5-4d06-a560-8b1e2f371922">

Additionally, workflows have been created using the Dataproc through which a temporary cluster and a job is created to process the data and push to the final big query tables. The workflows are set to run everyday with the help of cloud scheduler. Each cloud scheduler is set to trigger everyday at a particular time period (traffic data workflow : Everyday 10am EDT, crimes data workflow : Everyday at 11am EDT, crashes data workflow : Everyday 12:30pm EDT)

**Workflows**
<img width="1416" alt="Screenshot 2024-05-15 at 2 45 30 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/98a15f06-a9c0-4e64-917b-2f19f74ba1fa">

**Jobs**
<img width="1416" alt="Screenshot 2024-05-15 at 2 50 15 AM" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/147477465/b1ba5f58-682c-4b83-8554-277a8fd8320d">

## Storage
For our storage solution, we opted to utilize BigQuery for its capabilities and compatibility with our project requirements. In addition to storing our data in BigQuery, we structured the storage by creating a database called Montgomery Datasets and in that we created separate tables for each API: crashes, crimes, and traffic violations

**Crashes Dataset**
<img width="1106" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/67585d3a-ef3d-49fc-9848-47e617802702">

**Crimes Dataset**
<img width="1110" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/84313030-0a19-460f-9533-80ecb84e66b2">

**Traffic_Violations Dataset**
<img width="1118" alt="image" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/160145247/8ee2d1bb-05bd-4593-af94-525f82ea51a0">

## Analysis

In this project, we leveraged Looker Studio to analyze and visualize data across three key schemas: Crashes, Crimes, and traffic violations dataset, to derive actionable insights from complex information. Through a series of meaningful visualizations, such as trend analyses over time, geographical heatmaps, and distribution charts, we aim to illuminate patterns and trends that inform strategic decision-making. The dashboards created in Looker Studio not only highlight critical data points but also facilitate a deeper understanding of the underlying dynamics within each dataset.


-**Crimes Dashboard**

The Crimes dashboard delves into the rate and distribution of crimes over time and across categories, utilizing a heat map to visualize geographical crime hotspots and identify regions requiring heightened security measures. Detailed pie charts and bar graphs break down crime types and locations, offering stakeholders a clear view of predominant crime patterns and enabling more effective community policing and resource allocation strategies.


<img width="960" alt="Screenshot 2024-05-15 010321" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/c1f30f43-1aef-4704-8285-10adf1cb036b">

-**Crashes Dashboard**

This dashboard explores traffic crashes, with visualizations that track crash occurrences over time and analyze them by light conditions, collision types, and intersection configurations. It provides critical insights into the conditions under which most crashes occur, such as time of day or specific traffic setups, aiding in the design of safer roads and more informed urban planning. The hit-and-run analysis further highlights the urgency of addressing driver accountability and enhancing surveillance measures.

<img width="960" alt="Screenshot 2024-05-15 010247" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/0f64fe42-4fdd-4aaa-83ce-3c2627ac5d3b">


-**Traffic Violations Dashboard**

This dashboard presents a comprehensive analysis of traffic violations, categorized by gender, race, and case type to identify demographic patterns. A trend analysis chart provides insights into the fluctuation of violations over time, pinpointing potential seasonal or enforcement-related trends. Additionally, a geographic breakdown by city offers a detailed view of where most violations occur, assisting in targeted traffic enforcement and policy-making.


<img width="961" alt="Screenshot 2024-05-15 010342" src="https://github.com/sriyanaidu/Team_08_Final_Project/assets/63516410/04bdd7f8-fc12-494b-9cf2-5af9e00cb926">


**Business Questions**
