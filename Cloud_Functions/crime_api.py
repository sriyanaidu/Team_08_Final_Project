# Install the required libraries

import pandas as pd
from sodapy import Socrata
from google.cloud import storage
from datetime import datetime, date

# Function to retrieve data from Crime API
def retrieve_data():
    # Use Socrata to retrieve the required data
    client = Socrata("data.montgomerycountymd.gov", "gKC7o6XwSC7f3n9PKLMyF2SWW", username='gouthamp@umd.edu', password='zYw7cN4M9hUG23!')

    # Get the latest 50000 entries from API
    results = client.get("icn6-v9z3", limit=50000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df

# Function to upload data to a GCS bucket
def upload_to_gcs(data, storage_client):
    
    # Get current date and time
    current_time = datetime.now().replace(microsecond=0) 
    current_day = current_time.day 
    bucket = storage_client.bucket("crime_bucket_api")
    blob = bucket.blob(f"crimeapi/{current_day}/crimecapi_data_{current_time}.json")
    
    # Upload the data to blob
    blob.upload_from_string(data.to_json(orient="records"), content_type='application/json')

# HTTP Cloud Function
def main(request):
    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    # Get JSON data using requests
    request_json = request.get_json(silent=True)
    # Get query parameters using requests
    request_args = request.args

    # Determine 'name' from either JSON or query parameters
    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    
    # Retrieve data from crime API
    data_df = retrieve_data()

    # Upload data to Google Cloud Storage bucket
    upload_to_gcs(data_df, storage_client)

    return 'Data retrieved and uploaded to Google Cloud'.format(name)
