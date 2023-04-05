import os
from dotenv import load_dotenv
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine


def return_sql_engine() -> Engine:
    """
    Return string used for the database engine
    """
    load_dotenv("/.env")

    sf_account_name = os.environ.get("SNOWFLAKE_ACCOUNT_NAME")
    sf_admin_user_name = os.environ.get("SNOWFLAKE_ADMIN_USER_NAME")
    sf_admin_password = os.environ.get("SNOWFLAKE_ADMIN_PASSWORD")
    sf_authenticator = os.environ.get("SNOWFLAKE_AUTHENTICATOR")
    sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE")
    sf_role = os.environ.get("SNOWFLAKE_ROLE")
    # Database objects
    sf_database = "ALTERNATIVE_RISKS"
    sf_schema = "ALT_RISK"

    return create_engine(
        f"snowflake://{sf_admin_user_name}:{sf_admin_password}@{sf_account_name}"
        f"/{sf_database}/{sf_schema}?authenticator={sf_authenticator}&warehouse={sf_warehouse}&role={sf_role}"
    )

# print(get_sql_engine())
