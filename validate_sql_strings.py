import pandas as pd
from get_sql_engine import return_sql_engine


def validate_sql_query(sf_sql_query):
    """
    This section will test to ensure commands sent to snowflake
    database are not going to error
    """
    sf_sql_engine = return_sql_engine()
    try_test = False

    try:
        print("Starting run of sql query ")
        pcs_codes_df = pd.read_sql_query(sql=sf_sql_query, con=sf_sql_engine)  # , chunksize=chunk_size)
        try_test = True
    except Exception as e:
        print(f"something went wrong!, str({e})")
    finally:
        sf_sql_engine.dispose()
        print("sql query completed and sql_engine closed")
        try_test = True

    return try_test
