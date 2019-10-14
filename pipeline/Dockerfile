FROM jupyter/pyspark-notebook

USER root
# ENV PATH="${PATH};/rallyai/spark-etl-pipeline/drivers"
# ENV PYSPARK_SUBMIT_ARGS="--master local[2] pyspark-shell"

WORKDIR /rallyai/spark-etl-pipeline
COPY . . 

RUN sudo apt-get update
RUN sudo apt-get install libpq-dev python-dev -y
RUN pip install psycopg2 
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.6.jar

USER jovyan

EXPOSE 8888

CMD [ "jupyter", "notebook", "--allow-root" ]