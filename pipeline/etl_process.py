"""
RalliAI - UCSC CSE 115A - Fall 2019
"""

import os
import psycopg2
from pyspark.sql import SparkSession, DataFrameWriter
from pyspark.sql.types import (StructField, StructType, StringType,
                               IntegerType, FloatType, DateType)


def init_postgres_connection():
    """Init the connection to the Postgres database using env vars

    Returns:
        [cursor] -- [A cursor for the DB connection for running queries against]
    """
    db_host = "database"
    db_name = os.environ["POSTGRES_USER"]
    db_user = os.environ["POSTGRES_USER"]
    db_password = os.environ["POSTGRES_PASSWORD"]

    postgres_connection = psycopg2.connect(
        f"host={db_host} dbname={db_name} user={db_user} password={db_password}"
    )

    return postgres_connection.cursor()


def write_dataframe_to_postgres(arg_data_frame, table_name):
    """Loads an argues Spark dataframe to the PG database.

    Arguments:
        arg_data_frame {DataFrame} -- The dataframe who's contents will be written to the DB
        table_name {String} -- The DB table that will be written to
    """

    if os.environ.get("ENV") == "production":
        db_address = os.environ["DB_ADDRESS"]
        db_user = os.environ["POSTGRES_USER"]
        db_password = os.environ["POSTGRES_PASSWORD"]

        connection_string = f"jdbc:postgresql://{db_address}/{table_name}"
        connection_properties = {
            "driver": "org.postgresql.Driver",
            "user": db_user,
            "password": db_password,
        }

        arg_data_frame.write.jdbc(url=db_address,
                                  table=table_name,
                                  mode="overwrite",
                                  properties=connection_properties)
    else:
        arg_data_frame.write.jdbc(url="jdbc:postgresql://database:5432/docker",
                                  table=table_name,
                                  mode="overwrite",
                                  properties={
                                      "driver": 'org.postgresql.Driver',
                                      "user": "docker",
                                      "password": "docker"
                                  })


def generate_data_frame_from_csv(csv_file_path):
    """This method creates a DataFrame schema and then reads
       the values from an argued CSV file into a DataFrame.

    Arguments:
        csv_file_path {String} -- The relative path tot he CSV file to be read.

    Returns:
        DataFrame -- The new Spark DataFrame containign the files contents.
    """
    data_schema = [
        StructField("ticker", StringType(), True),
        StructField("open", FloatType(), True),
        StructField("close", FloatType(), True),
        StructField("adj_close", FloatType(), True),
        StructField("low", FloatType(), True),
        StructField("high", FloatType(), True),
        StructField("volume", FloatType(), True),
        StructField("date", DateType(), True)
    ]

    final_struct = StructType(fields=data_schema)

    data_frame = spark.read.csv(csv_file_path, schema=final_struct)
    data_frame = data_frame.withColumnRenamed("ticker", "symbol")
    data_frame = data_frame.withColumnRenamed("open", "opening_price")
    data_frame = data_frame.withColumnRenamed("close", "closing_price")
    data_frame = data_frame.withColumnRenamed("low", "lowest_price")
    data_frame = data_frame.withColumnRenamed("high", "highest_price")
    data_frame = data_frame.withColumn("volume_in_millions",
                                       data_frame["volume"] / 1000000)
    data_frame.createOrReplaceTempView("stocks")

    return data_frame


if __name__ == "__main__":
    # Init new Spark application session.
    spark_master = os.environ["SPARK_MASTER"]
    spark = SparkSession.builder \
        .master(spark_master) \
        .appName("rallyai_etl_pipeline") \
        .config("spark.jars", "/rallyai/spark-etl-pipeline/jars/postgresql-42.2.8.jar") \
        .config("spark.driver.memory", "7g") \
        .getOrCreate() \

    # Init new loggers
    log4jLogger = spark._jvm.org.apache.log4j
    log = log4jLogger.LogManager.getLogger(__name__)

    # Read the raw dataset from the CSV file
    raw_dataset_path = os.environ["CSV_FILE_PATH"]
    data_frame = generate_data_frame_from_csv(raw_dataset_path)

    # Print the schema to the console
    data_frame.printSchema()

    results = spark.sql(
        "SELECT * FROM stocks WHERE symbol IS NOT  NULL AND date IS NOT NULL")
    db_connection_cursor = init_postgres_connection()
    write_dataframe_to_postgres(results, "stocks")

    results.write.csv("model_training_data", mode="overwrite")
