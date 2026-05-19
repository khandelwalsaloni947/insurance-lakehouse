from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def standardize_text(df: DataFrame, columns: list) -> DataFrame:
    result = df
    for column_name in columns:
        result = result.withColumn(column_name, F.lower(F.trim(F.col(column_name))))
    return result

def cast_to_date(df: DataFrame, columns: list) -> DataFrame:
    result = df
    for column_name in columns:
        result = result.withColumn(column_name, F.to_date(F.col(column_name)))
    return result

def cast_to_double(df: DataFrame, columns: list) -> DataFrame:
    result = df
    for column_name in columns:
        result = result.withColumn(column_name, F.col(column_name).cast("double"))
    return result

def deduplicate_by_key(df: DataFrame, key_col: str) -> DataFrame:
    return df.dropDuplicates([key_col])
