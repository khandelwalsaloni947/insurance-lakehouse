from pyspark.sql import functions as F

def count_duplicate_grain(df, grain_columns):
    return df.groupBy(*grain_columns).count().filter(F.col("count") > 1).count()

def count_nulls(df, column_name):
    return df.filter(F.col(column_name).isNull()).count()
