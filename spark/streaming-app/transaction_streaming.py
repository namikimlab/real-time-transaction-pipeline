from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, col, when

# Spark Session
spark = SparkSession.builder \
    .appName("TransactionStreaming") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

# Schema
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

# Kafka Source
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Flatten location
flat_df = json_df.withColumn("latitude", col("location.lat")) \
                 .withColumn("longitude", col("location.lon")) \
                 .drop("location")

# Simple Fraud Logic
fraud_df = flat_df.withColumn("is_fraud", when(
    (col("amount") > 3000) |
    (col("is_foreign") == True) |
    (col("latitude") > 90) | (col("latitude") < -90) | 
    (col("longitude") > 180) | (col("longitude") < -180),
    True
).otherwise(False))

# Write to Postgres
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/transactions") \
        .option("dbtable", "fact_transaction") \
        .option("user", "admin") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

query = fraud_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .start()

query.awaitTermination()
