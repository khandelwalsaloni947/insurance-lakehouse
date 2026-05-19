from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def add_customer_hashes(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("customer_hash", F.sha2(F.col("customer_id").cast("string"), 256))
          .withColumn("email_hash", F.sha2(F.lower(F.trim(F.col("email"))), 256))
          .withColumn("phone_hash", F.sha2(F.trim(F.col("phone_number")), 256))
    )

def remove_direct_customer_pii(df: DataFrame) -> DataFrame:
    columns_to_drop = ["email", "phone_number", "street"]
    existing = [c for c in columns_to_drop if c in df.columns]
    return df.drop(*existing)

def add_customer_age(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "customer_age",
        F.floor(F.months_between(F.current_date(), F.to_date(F.col("date_of_birth"))) / 12)
    )
