import snowflake.connector
import os
from dotenv import load_dotenv
from validate_sql_strings import validate_sql_query

load_dotenv("/qa_project/.env")


def sf_connection_string():
    """
    This will create the connection string that can be used
    for all calls to the snowflake database
    """
    conn = snowflake.connector.connect(
        user=os.environ.get("SNOWFLAKE_ADMIN_USER_NAME"),
        password=os.environ.get("SNOWFLAKE_ADMIN_PASSWORD"),
        account=os.environ.get("SNOWFLAKE_ACCOUNT_NAME"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
        database=os.environ.get("SNOWFLAKE_DATABASE"),
        schema=os.environ.get("SNOWFLAKE_DATABASE_SCHEMA")
    )
    return conn


def insert_raw_with_json():
    """
    Once the import of the spreadsheets are complete
    this will add the relevant data into the data model

    """
    sql_step_1 = """INSERT INTO ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_XL_ROW
        (IMPORT_ROW_NUMBER
            , FILENAME
            , SHA256_FILE_HASH
            , EXCEL_DATE_MODE
            , SHEET_NAME
            , ROW_JSON)
        SELECT IMPORT_ROW_NUMBER
            , FILENAME
            , SHA256_FILE_HASH
            , EXCEL_DATE_MODE
            , SHEET_NAME
            , PARSE_JSON(ROW_JSON)
        FROM ALTERNATIVE_RISKS.alt_risk.ALT_RISK_XL_ROW_STAGE;"""

    sql_step_2 = """INSERT INTO ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME
        (NO_OF_RECORDS_FILE, FILENAME, SHA256_FILE_HASH, REPORTING_PERIOD, COUNT_OF_SHEETS)
        SELECT COUNT(S_v.*) NO_OF_RECORDS
            , S_v.FILENAME
            , S_v.SHA256_FILE_HASH
            , CURRENT_TIMESTAMP AS REPORTING_PERIOD
            , COUNT(DISTINCT(S_V.SHEET_NAME)) AS SHEET_NAME
        FROM ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_XL_ROW S_v
        WHERE S_v.SHA256_FILE_HASH NOT IN (SELECT SHA256_FILE_HASH
                                        FROM ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME)
        GROUP BY
        S_v.SHA256_FILE_HASH
        ,S_v.FILENAME
        QUALIFY ROW_NUMBER() OVER (PARTITION BY S_v.SHA256_FILE_HASH, CURRENT_TIMESTAMP ORDER BY SHA256_FILE_HASH) = 1;"""

    sql_step_3 = """INSERT INTO ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME_SHEETNAME 
            (FILENAME_ID,
            IMPORT_ROW_NUMBER,
            BORDEREAU_TYPE_ID,
            SHEET_NAME)
            SELECT DISTINCT 
                SV1.FILENAME_ID 
                , v1.IMPORT_ROW_NUMBER
                , CASE WHEN ROW_JSON:"0"::VARCHAR='GROSS PREMIUM' 
                    THEN 1 
                    ELSE 0 END AS BORDEREAU_TYPE_ID
                , v1.SHEET_NAME
            FROM ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_XL_ROW v1
            INNER JOIN ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME sv1 
            ON sv1.SHA256_FILE_HASH = v1.SHA256_FILE_HASH
            AND sv1.FILEnAme = v1.FILENAME
            WHERE v1.IMPORT_ROW_NUMBER BETWEEN 0 AND 5 
            AND BORDEREAU_TYPE_ID = 1;"""

    sql_step_4 = """INSERT INTO ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME_SHEETNAME_HEADER
        (FILENAME_ID
            , SHEET_NAME_ID
            , IMPORT_ROW_ID
            , HEADER_NAME
            , HEADER_VALUE)
        SELECT F_V.FILENAME_ID
            , FS_V.SHEET_NAME_ID 
            , XL_V.IMPORT_ROW_NUMBER
            , XL_V.ROW_JSON:"0"::VARCHAR AS HEADER_NAME 
            , XL_V.ROW_JSON:"1"::VARCHAR AS HEADER_VALUE
        FROM ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_XL_ROW XL_V
        INNER JOIN ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME F_V
        ON F_V.SHA256_FILE_HASH = XL_V.SHA256_FILE_HASH
        AND F_V.FILENAME = XL_V.FILENAME 
        INNER JOIN ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME_SHEETNAME FS_V
        ON FS_V.FILENAME_ID = F_V.FILENAME_ID 
        AND FS_V.SHEET_NAME = XL_V.SHEET_NAME 
        WHERE XL_V.IMPORT_ROW_NUMBER BETWEEN 0 AND 5;"""

    sql_step_5 = """INSERT INTO ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME_SHEETNAME_HEADER
            (FILENAME_ID
                , SHEET_NAME_ID
                , IMPORT_ROW_ID
                , HEADER_NAME
                , HEADER_VALUE)
            SELECT F_V.FILENAME_ID
                , FS_V.SHEET_NAME_ID 
                , XL_V.IMPORT_ROW_NUMBER
                , XL_V.ROW_JSON:"0"::VARCHAR AS HEADER_NAME 
                , XL_V.ROW_JSON:"1"::VARCHAR AS HEADER_VALUE
            FROM ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_XL_ROW XL_V
            INNER JOIN ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME F_V
            ON F_V.SHA256_FILE_HASH = XL_V.SHA256_FILE_HASH
            AND F_V.FILENAME = XL_V.FILENAME 
            INNER JOIN ALTERNATIVE_RISKS.ALT_RISK.ALT_RISK_FILENAME_SHEETNAME FS_V
            ON FS_V.FILENAME_ID = F_V.FILENAME_ID 
            AND FS_V.SHEET_NAME = XL_V.SHEET_NAME 
            WHERE XL_V.IMPORT_ROW_NUMBER BETWEEN 0 AND 5;"""

    conn = sf_connection_string()

    cursor = conn.cursor()

    if validate_sql_query(sql_step_1):
        cursor.execute(sql_step_1)

    if validate_sql_query(sql_step_2):
        cursor.execute(sql_step_2)

    if validate_sql_query(sql_step_3):
        cursor.execute(sql_step_3)

    if validate_sql_query(sql_step_4):
        cursor.execute(sql_step_4)

    if validate_sql_query(sql_step_5):
        cursor.execute(sql_step_5)

    cursor.close()

    print("Inserts completed")
