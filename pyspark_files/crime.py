from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import to_timestamp
from google.cloud import storage

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("CrimesApp") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.22.0") \
    .getOrCreate()

# Construct folder path for the current day
from datetime import datetime
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = f"gs://crime_bucket_api/crimeapi/{current_date}/"

destination_table = "umd-inst767.montgomery_datasets.crimes"
gcs_bucket = "pyspark_bucket_inst767"

results_df = spark.read.option("header", "true").json(folder_path)

columns_to_drop = [
    ":@computed_region_vu5j_pcmz", ":@computed_region_tx5f_5em3",
    ":@computed_region_kbsp_ykn9", ":@computed_region_d7bw_bq6x",
    ":@computed_region_rbt8_3x7n", ":@computed_region_a9cs_3ed7",
    ":@computed_region_r648_kzwt", ":@computed_region_d9ke_fpxt",
    ":@computed_region_6vgr_duib", "geolocation", "end_date",
    "street_prefix_dir", "street_suffix_dir"
]
results_df = results_df.drop(*columns_to_drop)

# Replace "n/a" with blank (empty string)
results_df = results_df.na.replace("N/A", "", subset=results_df.columns)

# Convert latitude and longitude to float type
results_df = results_df.withColumn("latitude", col("latitude").cast("float")) \
    .withColumn("longitude", col("longitude").cast("float"))

# Handle missing values for other columns
columns_with_missing_values = [
    "date", "district", "location", "state", "zip_code",
    "address_number", "address_street", "street_type"
]
for column in columns_with_missing_values:
    results_df = results_df.na.fill("", [column])

# Assuming 'date' is the name of the string column representing date-time
results_df = results_df.withColumn("date", to_timestamp("date", "yyyy-MM-dd HH:mm:ss"))

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

