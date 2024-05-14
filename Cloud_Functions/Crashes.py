# Install the required libraries

import pandas as pd
from sodapy import Socrata
from google.cloud import storage
from datetime import datetime, date

# Function to retrieve data from Crashes API
def retrieve_data():
    # Use Socrata to retrieve the required data
    client = Socrata("data.montgomerycountymd.gov", "yNz7zg5OJIAyFFzl0msRnXVqs", username='reddysakshi27@gmail.com', password='greysAnatomy@1234')

    
    # Get the latest 50000 entries from API
    results = client.get("bhju-22kf", limit=50000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df

# Function to upload data to a GCS bucket
def upload_to_gcs(data, storage_client):
    # Get current date and time
    current_day = date.today().isoformat()
    current_time = datetime.now().isoformat(timespec='seconds').replace(':', '-')

    # Define the file path
    file_path = f"crashesapi/{current_day}"
    file_name = f"crashescapi_data_{current_time}.json"
    bucket = storage_client.bucket("crashesumd")
    blob = bucket.blob(f"{file_path}/{file_name}")

    # Upload the data to blob
    blob.upload_from_string(data.to_json(orient="records"), content_type='application/json')

# HTTP Cloud Function
def main(request):
    # Initialize a Google Cloud Storage client
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
    
    # Retrieve data from Crashes API
    data_df = retrieve_data()

    # Upload data to Google Cloud Storage bucket
    upload_to_gcs(data_df, storage_client)

    return 'Data retrieved and uploaded to Google Cloud.'.format(name)

