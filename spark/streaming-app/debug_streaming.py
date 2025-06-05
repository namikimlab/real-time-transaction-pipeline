# Minimal debug version to test Kafka connectivity
from pyspark.sql import SparkSession
import os

print("🔍 Debug mode: Testing Kafka connectivity only")

# Create Spark session
spark = SparkSession.builder \
    .appName("DebugKafkaConnection") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("📡 Attempting to connect to Kafka...")

# Read raw Kafka stream
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

print("✅ Kafka connection established")

# Just show raw data to verify connectivity
debug_query = raw_df.selectExpr(
    "CAST(key AS STRING) as message_key",
    "CAST(value AS STRING) as message_value", 
    "topic",
    "partition",
    "offset",
    "timestamp"
).writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 10) \
    .trigger(processingTime='5 seconds') \
    .start()

print("🎯 Debug query started - watching for messages...")
print("💡 If you see messages below, Kafka connection is working!")

try:
    debug_query.awaitTermination()
except KeyboardInterrupt:
    print("\n🛑 Stopping debug query...")
    debug_query.stop()
    spark.stop()
    print("✨ Debug session ended")