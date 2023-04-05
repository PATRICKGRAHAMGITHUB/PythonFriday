import pandas as pd
import os
import xlrd
import re
from filehash import FileHash
from get_sql_engine import return_sql_engine
from check_file_type import validate_xl_file_type


def xl_to_snowflake():
    """
    This section actually imports all xls spreadsheets from

    C/:xl/ into xl_row_stage on the snowflake database
    """
    sql_engine = return_sql_engine()

    sf_tablename = "ALT_RISK_XL_ROW_STAGE"

    filenames = [
        f
        for f in os.listdir(path="/xl")
        if re.compile(r"(?!~\$).*.xls", re.IGNORECASE).match(f)
    ]

    for filename in filenames:
        # calculate file hash
        sha256_file_hash = FileHash(hash_algorithm="sha256").hash_file(
            filename="/xl/" + filename
        )

        if validate_xl_file_type(filename):
            workbook = xlrd.open_workbook(filename="/xl/" + filename)
            print(f'{filename} is being imported')

        for sheet_name in workbook.sheet_names():
            df = pd.read_excel(io=workbook, sheet_name=sheet_name, header=None)

            # collapse columns into JSON
            df["ROW_JSON"] = df.agg(
                func=lambda series: series.to_json(orient="index"), axis="columns"
            )

            df["IMPORT_ROW_NUMBER"] = df.index

            # TODO break these into separate tables XL_WORKBOOK, XL_SHEET, XL_ROW
            df = df.assign(
                FILENAME=filename,
                SHA256_FILE_HASH=sha256_file_hash,
                EXCEL_DATE_MODE=workbook.datemode,
                SHEET_NAME=sheet_name,
            )

            # pick only the columns we're interested in
            df = df[
                [
                    "IMPORT_ROW_NUMBER",
                    "FILENAME",
                    "SHA256_FILE_HASH",
                    "EXCEL_DATE_MODE",
                    "SHEET_NAME",
                    "ROW_JSON",
                ]
            ]

            # TODO optimise method and chunkisze parameters
            df.to_sql(
                name=sf_tablename, con=sql_engine, schema=sf_schema, if_exists="append", index=False, chunksize=16384
            )

    sql_engine.dispose()

