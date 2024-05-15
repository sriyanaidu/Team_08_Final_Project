from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp
from google.cloud import storage
from datetime import datetime

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CrashesApp") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.22.0") \
    .getOrCreate()

# Construct folder path for the current day
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = f"gs://crashesumd/crashesapi/{current_date}/"

destination_table = "umd-inst767.montgomery_datasets.crashes"
gcs_bucket = "pyspark_bucket_inst767"

# Drop unnecessary columns
columns_to_drop = ["off_road_description", "related_non_motorist", "non_motorist_substance_abuse", "lane_type", 'geolocation', ':@computed_region_vu5j_pcmz',
      ':@computed_region_tx5f_5em3', ':@computed_region_kbsp_ykn9',':@computed_region_d7bw_bq6x', ':@computed_region_rbt8_3x7n',':@computed_region_a9cs_3ed7', ':@computed_region_r648_kzwt',
      ':@computed_region_6vgr_duib']

results_df = spark.read.option("header", "true").json(folder_path)
results_df = results_df.drop(*columns_to_drop)

results_df = results_df.na.replace("N/A", "", subset=results_df.columns)

def clean_invalid_lat_lon(df, columns):
    for column in columns:
        df = df.filter(df[column].isNotNull() & (df[column] != 0.0))
    return df

# Clean latitude and longitude columns
results_df = clean_invalid_lat_lon(results_df, ['latitude', 'longitude'])

# For simplicity, let's drop rows with any missing values
results_df = results_df.na.drop()

# Assuming 'crash_date_time' is the name of the string column representing date-time
results_df = results_df.withColumn("crash_date_time", to_timestamp("crash_date_time", "yyyy-MM-dd HH:mm:ss"))

# Remove duplicates
results_df = results_df.dropDuplicates()

# Finally, you can show the cleaned DataFrame
results_df.show()

# Writing DF to BigQuery
results_df.write.format('bigquery') \
    .option('table', destination_table) \
    .option('temporaryGcsBucket', gcs_bucket) \
    .mode('overwrite') \
    .save()

# Creating cloud storage client
storage_client = storage.Client()

# Stop Spark session
spark.stop()
