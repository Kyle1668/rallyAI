"""
RalliAI - UCSC CSE 115A - Fall 2019
Kyle O'Brien - kdobrien@ucsc.edu
"""

import os
import psycopg2
from pyspark.sql import SparkSession
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
    arg_data_frame.write.jdbc(url="jdbc:postgresql://database:5432/docker",
                              table=table_name,
                              mode="overwrite",
                              properties={
                                  "driver": 'org.postgresql.Driver',
                                  "user": os.environ["POSTGRES_USER"],
                                  "password": os.environ["POSTGRES_PASSWORD"]
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
        StructField("open", FloatType()),
        StructField("close", FloatType()),
        StructField("adj_close", FloatType()),
        StructField("low", FloatType()),
        StructField("high", FloatType()),
        StructField("volume", FloatType()),
        StructField("date", DateType())
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
    """Program Driver
    """
    spark = SparkSession.builder \
        .master("local[4]") \
        .appName("rallyai_etl_pipeline") \
        .config("spark.jars", "/rallyai/spark-etl-pipeline/jars/postgresql-42.2.8.jar") \
        .getOrCreate() \

    raw_dataset_path = os.environ["CSV_FILE_PATH"]
    data_frame = generate_data_frame_from_csv(raw_dataset_path)

    # Print the schema to the console
    data_frame.printSchema()

    results = spark.sql("SELECT * FROM stocks WHERE symbol='MSFT'")
    db_connection_cursor = init_postgres_connection()
    write_dataframe_to_postgres(results, "stocks")