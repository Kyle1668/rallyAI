"""
RalliAI - UCSC CSE 115A - Fall 2019
"""

# env vars with sample values
# SPARK_MASTER=local[8]
# POSTGRES_USER=docker
# POSTGRES_PASSWORD=docker
# DB_TABLE=docker
# DB_ADDRESS=database:5432
# CSV_FILE_PATH=sample_data/historical_stock_prices.csv

import os
import psycopg2
from pyspark.sql import SparkSession, DataFrameWriter
from pyspark.sql.types import (StructField, StructType, StringType,
                               IntegerType, FloatType, DateType)


def init_postgres_connection():
    """Init the connection to the Postgres database using env vars

    Returns:
        [cursor] -- [Cursor for the DB connection for running queries against]
    """
    db_host = "database"
    db_name = os.environ["POSTGRES_USER"]
    db_user = os.environ["POSTGRES_USER"]
    db_password = os.environ["POSTGRES_PASSWORD"]

    connection_config = f"host={db_host} dbname={db_name} user={db_user} password={db_password}"
    postgres_connection = psycopg2.connect(connection_config)

    return postgres_connection.cursor()


def write_dataframe_to_postgres(arg_data_frame, table_name):
    """Loads an argues Spark dataframe to the PG database.

    Arguments:
        arg_data_frame {DataFrame} -- The dataframe who's contents will be
        written to the DB table_name {String} -- The DB table
        that will be written to
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
    final_struct = StructType(fields=data_schema)
    data_frame = spark.read.csv(csv_file_path, inferSchema=True, header=True)
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
    # query = "SELECT * FROM stocks WHERE company_name IS NOT  NULL AND market_date IS NOT NULL"
    # results = spark.sql(query)

    # Write to Postgres
    db_connection_cursor = init_postgres_connection()

    # Write to CSV
    write_dataframe_to_postgres(data_frame, "stocks")
    data_frame.write.csv("model_training_data", mode="overwrite")
