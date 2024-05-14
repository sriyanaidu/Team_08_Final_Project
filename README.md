# Big Data Final Project
INST 767: Big Data Analytics  
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

Limitations of the data: information may not be verified due to investigations, classifications may be changed in the future.

**Crash Reporting - Incidents Data**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/bhju-22kf)

This API provides general information about each collision and details of all traffic collisions occuring on county and local roadways in Montgomery County. Data incorporates information from the Automated Crash Reporting System (ACRS), as well as information from Montgomery County Police, Gaithersburg Police, Rockville Police, and the Maryland-National Capital Park Police.

Limitations of the data: information is based on preliminary reporting and may not be verified, data may change at a later date after further investigation.

Updated: Weekly

**Traffic Violations**: [link to documentation](https://dev.socrata.com/foundry/data.montgomerycountymd.gov/4mse-ku6q)

This API contains information about traffic violations from all electronic traffic violations issued within Montgomery County.

Limitations of the data: any information that can be used to uniquely identify the vehicle, vehicle owner, or the office issuing the violation is not published.

Updated: Daily

## Transform
- Implemented data transformation using PySpark on DataProc.
- Transformed raw data from the ingest stage into a unified data model suitable for analysis.
- Scheduled to run periodically to align with ingest timing.
  
## Storage
- Utilized BigQuery as the storage solution due to its scalability and compatibility.
- Structured the data model logically, with separate tables for crime, crash, and traffic violation data.
- Stored all collected data securely and made it easily queryable in BigQuery.
  
## Analysis

## Management
