FROM jupyter/pyspark-notebook

USER root
# ENV PATH="${PATH};/rallyai/spark-etl-pipeline/drivers"
# ENV PYSPARK_SUBMIT_ARGS="--master local[2] pyspark-shell"

WORKDIR /rallyai/spark-etl-pipeline
COPY . . 

RUN sudo apt-get update
RUN sudo apt-get install libpq-dev python-dev dos2unix vim -y
RUN pip install psycopg2 
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.6.jar

RUN dos2unix etl_process.py

USER jovyan

EXPOSE 8888

# Uncomment to run via a Jupyter Notebook
# CMD [ "jupyter", "notebook", "--allow-root" ]

CMD [ "/usr/local/spark/bin/spark-submit", "--conf", "spark.jars=jars/postgresql-42.2.8.jar", "etl_process.py" ]