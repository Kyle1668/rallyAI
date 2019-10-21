import os
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.types import (StructField, StructType, StringType,
                               IntegerType, FloatType, DateType)


def init_postgres_connection():
    db_host = "database"
    db_name = os.environ["POSTGRES_USER"]
    db_user = os.environ["POSTGRES_USER"]
    db_password = os.environ["POSTGRES_PASSWORD"]

    postgres_connection = psycopg2.connect(
        f"host={db_host} dbname={db_name} user={db_user} password={db_password}"
    )

    return postgres_connection.cursor()


def write_dataframe_to_postgres(arg_data_frame, table_name):
    arg_data_frame.write.jdbc(url="jdbc:postgresql://database:5432/docker",
                              table=table_name,
                              mode="overwrite",
                              properties={
                                  "driver": 'org.postgresql.Driver',
                                  "user": "docker",
                                  "password": "docker"
                              })


def generate_data_frame_from_csv(csv_file_path):
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
    spark = SparkSession.builder \
        .master("local[4]") \
        .appName("Basics") \
        .config("spark.jars", "/rallyai/spark-etl-pipeline/jars/postgresql-42.2.8.jar") \
        .getOrCreate() \

    data_frame = generate_data_frame_from_csv("historical_stock_prices.csv")
    results = spark.sql("SELECT * FROM stocks WHERE symbol='MSFT'")
    db_connection_cursor = init_postgres_connection()
    write_dataframe_to_postgres(results, "stocks")