def preview_view(spark, full_view_name: str, limit: int = 20):
    return spark.table(full_view_name).limit(limit)

def view_row_count(spark, full_view_name: str) -> int:
    return spark.table(full_view_name).count()
