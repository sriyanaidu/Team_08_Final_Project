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

## Business Problem

## Project Description

# Application Architecture 

## Extract

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
  - The mode was set to "overwrite" to replace any existing data in the destination tables. This ensures that the BigQuery tables are updated with the latest cleaned data, maintaining data consistency and accuracy for subsequent analysis.

## Storage

## Analysis

## Management
