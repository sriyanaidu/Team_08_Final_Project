from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import to_timestamp
from google.cloud import storage
from datetime import datetime

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("TrafficViolationsApp") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.22.0") \
    .getOrCreate()

# Construct folder path for the current day
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = f"gs://inst767trafficviolationsbucket/trafficviolationsapi/{current_date}/"
destination_table = "umd-inst767.montgomery_datasets.traffic_violations"
gcs_bucket = "pyspark_bucket_inst767"

results_df = spark.read.option("header", "true").json(folder_path)

# Remove specified columns
columns_to_remove = [
    ":@computed_region_d7bw_bq6x", ":@computed_region_kbsp_ykn9",
    ":@computed_region_rbt8_3x7n", ":@computed_region_tx5f_5em3",
    ":@computed_region_vu5j_pcmz", "geolocation", "agency", "hazmat"
]
results_df = results_df.drop(*columns_to_remove)

# Define functions to clean specific columns
def clean_missing_values(df, column):
    return df.na.drop(subset=[column])

def clean_inconsistent_values(df, column):
    return df.withColumn(column, when(df[column] == "unknown", None).otherwise(df[column]))

def clean_invalid_lat_lon(df, columns):
    for column in columns:
        df = df.filter(df[column].isNotNull() & (df[column] != 0))
    return df

# Apply cleaning functions to other columns
columns_to_clean = [
    'article', 'belts', 'location', 'race', 'arrest_type',
    'charge', 'subagency', 'date_of_stop', 'color', 'vehicle_type',
    'accident', 'state', 'violation_type', 'latitude', 'driver_state',
    'model', 'personal_injury', 'fatal', 'year', 'property_damage',
    'gender', 'driver_city', 'longitude', 'alcohol',
    'time_of_stop', 'commercial_vehicle', 'make', 'work_zone',
    'dl_state', 'contributed_to_accident', 'commercial_license'
]

for column in columns_to_clean:
    results_df = clean_inconsistent_values(results_df, column)
    results_df = clean_missing_values(results_df, column)

# Clean latitude and longitude columns
results_df = clean_invalid_lat_lon(results_df, ['latitude', 'longitude'])

# Assuming 'date_of_stop' is the name of the string column representing date-time
results_df = results_df.withColumn("date_of_stop", to_timestamp("date_of_stop", "yyyy-MM-dd HH:mm:ss"))

# Display cleaned DataFrame
results_df.show()

# Writing DF to BigQuery
results_df.write.format('bigquery') \
    .option('table', destination_table) \
    .option('temporaryGcsBucket', gcs_bucket) \
    .mode('overwrite') \
    .save()

# Creating cloud storage client
storage_client = storage.Client()

# Finally, stop the SparkSession
spark.stop()
