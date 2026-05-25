def find_exposed_pii(columns, pii_fields):
    normalized_columns = {c.lower() for c in columns}
    return [field for field in pii_fields if field.lower() in normalized_columns]
