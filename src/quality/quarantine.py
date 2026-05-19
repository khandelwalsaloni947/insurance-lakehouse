from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def build_quarantine_df(df: DataFrame, record_id_col: str, source_table: str, error_reason: str, severity: str = "HIGH") -> DataFrame:
    return (
        df.withColumn("record_id", F.col(record_id_col).cast("string"))
          .withColumn("source_table", F.lit(source_table))
          .withColumn("error_reason", F.lit(error_reason))
          .withColumn("error_severity", F.lit(severity))
          .withColumn("quarantine_timestamp", F.current_timestamp())
          .withColumn("original_record_json", F.to_json(F.struct(*[F.col(c) for c in df.columns])))
          .select(
              "record_id",
              "source_table",
              "error_reason",
              "error_severity",
              "quarantine_timestamp",
              "source_file_name",
              "ingest_run_id",
              "original_record_json"
          )
    )
