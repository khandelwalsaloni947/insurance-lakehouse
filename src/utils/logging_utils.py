def log_table_counts(dataset_name: str, bronze_count: int, silver_count: int, quarantine_count: int):
    print("=" * 80)
    print(f"Dataset: {dataset_name}")
    print(f"Bronze rows: {bronze_count}")
    print(f"Silver rows: {silver_count}")
    print(f"Quarantine rows: {quarantine_count}")
    print("=" * 80)
