# Reads Kafka stream in near real-time
# Parses transaction records
# Runs fraud detection logic (business rules on-the-fly)
# Writes each record into fact_transaction in Postgres

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, col, when, current_timestamp, count, expr, to_timestamp
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB", "transactions")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

print("🚀 Starting Spark Streaming Application...")
print(f"📡 Kafka Bootstrap Servers: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"🗄️ PostgreSQL Database: {POSTGRES_DB}")

# Spark Session
spark = SparkSession.builder \
    .appName("TransactionStreaming") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schema definition
schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("customer_id", StringType()),
    StructField("merchant_id", StringType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("location", StructType([
        StructField("lat", DoubleType()),
        StructField("lon", DoubleType())
    ])),
    StructField("device_id", StringType()),
    StructField("payment_method", StringType()),
    StructField("is_foreign", BooleanType())
])

print("📊 Connecting to Kafka stream...")

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

print("✅ Connected to Kafka successfully")

# Parse Kafka JSON
json_df = df.selectExpr("CAST(value AS STRING)", "timestamp as kafka_timestamp", "offset", "partition") \
    .select(from_json(col("value"), schema).alias("data"), "kafka_timestamp", "offset", "partition") \
    .select("data.*", "kafka_timestamp", "offset", "partition")

# Write to Postgres inside foreachBatch
def write_to_postgres(batch_df, batch_id):
    try:
        print(f"\n📦 Processing batch {batch_id} with {batch_df.count()} records")

        # Flatten location
        batch_df = batch_df.withColumn("latitude", col("location.lat")) \
                           .withColumn("longitude", col("location.lon")) \
                           .withColumn("processing_time", current_timestamp()) \
                           .drop("location")

        # Apply fraud detection logic
        batch_df = batch_df.withColumn("is_fraud", when(
            (col("amount") > 3000) |
            (col("is_foreign") == True) |
            (col("latitude") > 90) | (col("latitude") < -90) | 
            (col("longitude") > 180) | (col("longitude") < -180),
            True
        ).otherwise(False))

        # Timestamp parsing and cleaning
        batch_df = batch_df.withColumn(
            "timestamp_clean",
            expr("left(timestamp, 23)")
        ).withColumn(
            "timestamp_parsed",
            to_timestamp(col("timestamp_clean"), "yyyy-MM-dd'T'HH:mm:ss.SSS")
        )

        # Final dataframe for insertion
        final_df = batch_df.select(
            col("transaction_id"),
            col("timestamp_parsed").alias("timestamp"),
            col("customer_id"),
            col("merchant_id"),
            col("amount").cast("decimal(10,2)"),
            col("currency"),
            col("latitude"),
            col("longitude"),
            col("device_id"),
            col("payment_method"),
            col("is_foreign"),
            col("is_fraud")
        )

        # Debug output
        final_df.printSchema()
        final_df.show(5, truncate=False)

        # Write to Postgres
        properties = {
            "user": POSTGRES_USER,
            "password": POSTGRES_PASSWORD,
            "reWriteBatchedInserts": "true"
        }

        final_df.write \
            .mode("append") \
            .jdbc(
                url=f"jdbc:postgresql://postgres:5432/{POSTGRES_DB}",
                table="fact_transaction",
                properties=properties
            )

        print(f"✅ Successfully wrote batch {batch_id} to PostgreSQL")

    except Exception as e:
        print(f"❌ Failed to write batch {batch_id}: {str(e)}")
        print("🔄 Continuing with next batch...")

# Start streaming query to Postgres
postgres_query = json_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "/tmp/checkpoints/postgres") \
    .trigger(processingTime='5 seconds') \
    .queryName("postgres_writer") \
    .start()

print("🎯 Streaming started!")
print("🛑 Press Ctrl+C to stop...")

try:
    postgres_query.awaitTermination()
except KeyboardInterrupt:
    print("\n🛑 Stopping streaming query...")
    postgres_query.stop()
finally:
    spark.stop()
    print("🏁 Spark session ended")
