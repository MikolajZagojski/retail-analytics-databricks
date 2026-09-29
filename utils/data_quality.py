from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()

def check_table_row_counts(catalog,schema):
    """Count rows in every table in the given catalog.schema; flag empty ones."""
    tables = spark.sql(f"SHOW TABLES IN {catalog}.{schema}").collect()
    results = []

    for row in tables:
        table_name = row['tableName']
        count = spark.sql(f"SELECT count(*) AS cnt FROM {catalog}.{schema}.{table_name}").collect()[0]["cnt"]
        status = "EMPTY" if count == 0 else "OK"
        results.append((table_name,count,status))
    return spark.createDataFrame(results,["table_name","row_count","status"])

    
