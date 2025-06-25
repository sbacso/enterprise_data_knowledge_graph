def verify_schema(sch_defined, schema):
    col_defined = set(sch_defined.columns)
    col = set(schema.columns)
    if col_defined == col:
        print("The schemas are aligned.")
    else:
        print(col_defined - col, col - col_defined)
