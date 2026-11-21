from pyspark import pipelines as dp
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Event Hubs configuration
EH_NAMESPACE = "UberDe"
EH_NAME = "ubertopic"

# Get connection string from Spark configuration
EH_CONN_STR = spark.conf.get("connection_string")

# Kafka configuration
KAFKA_OPTIONS = {
    "kafka.bootstrap.servers": f"{EH_NAMESPACE}.servicebus.windows.net:9093",

    "subscribe": EH_NAME,

    "kafka.sasl.mechanism": "PLAIN",

    "kafka.security.protocol": "SASL_SSL",

    "kafka.sasl.jaas.config":
        f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{EH_CONN_STR}";',

    "kafka.request.timeout.ms": 10000,

    "kafka.session.timeout.ms": 10000,

    "maxOffsetsPerTrigger": 10000,

    "failOnDataLoss": "true",

    "startingOffsets": "earliest"
}


# Read streaming data from Azure Event Hubs
@dp.table
def rides_raw():

    df = (
        spark.readStream
        .format("kafka")
        .options(**KAFKA_OPTIONS)
        .load()
    )

    # Convert binary value column into string
    df = df.withColumn(
        "rides",
        col("value").cast("string")
    )

    return df
