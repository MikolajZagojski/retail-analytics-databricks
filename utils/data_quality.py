from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()


def _get_table_names(catalog, schema, tables=None):
    """Return table names in catalog.schema, optionally filtered to the given list."""
    all_tables = spark.sql(f"SHOW TABLES IN {catalog}.{schema}").collect()
    table_names = [t["tableName"] for t in all_tables]

    if tables is not None:
        table_names = [t for t in table_names if t in tables]

    return table_names


def check_table_row_counts(catalog, schema, tables=None):
    """Count rows in every table in the given catalog.schema; flag empty ones."""
    results = []
    for table_name in _get_table_names(catalog, schema, tables):
        count = spark.sql(f"SELECT count(*) AS cnt FROM {catalog}.{schema}.{table_name}").collect()[0]["cnt"]
        status = "EMPTY" if count == 0 else "OK"
        results.append((table_name, count, status))

    return spark.createDataFrame(results, ["table_name", "row_count", "status"])


def check_null_counts(catalog, schema, tables=None):
    """Count NULLs in every column of the given tables (or all tables if none specified)."""
    results = []
    for table_name in _get_table_names(catalog, schema, tables):
        columns = spark.sql(f"SHOW COLUMNS IN {catalog}.{schema}.{table_name}").collect()
        column_names = [c["col_name"] for c in columns if c["col_name"] != "_rescued_data"]

        select_expr = ", ".join(
            f"SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS {col}" for col in column_names
        )
        row = spark.sql(f"SELECT {select_expr} FROM {catalog}.{schema}.{table_name}").collect()[0]

        for col in column_names:
            results.append((table_name, col, row[col]))

    return spark.createDataFrame(results, ["table_name", "column_name", "null_count"])


def check_rescued_data(catalog, schema, tables=None):
    """Count rows with non-empty _rescued_data, i.e. rows that did not fit the schema during ingestion."""
    results = []
    for table_name in _get_table_names(catalog, schema, tables):
        columns = spark.sql(f"SHOW COLUMNS IN {catalog}.{schema}.{table_name}").collect()
        column_names = [c["col_name"] for c in columns]

        if "_rescued_data" not in column_names:
            continue

        count = spark.sql(f"""
            SELECT COUNT(*) AS cnt
            FROM {catalog}.{schema}.{table_name}
            WHERE _rescued_data IS NOT NULL
        """).collect()[0]["cnt"]
        status = "OK" if count == 0 else "CHECK"
        results.append((table_name, count, status))

    return spark.createDataFrame(results, "table_name string, rescued_rows long, status string")
    

    

