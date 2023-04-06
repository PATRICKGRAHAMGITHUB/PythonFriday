# Introduction
This project is London Market's Alternative Risk Bordereau input proof of concept for QA Python project
...

# Getting started for developers
The build for the Alternative Risk runs on Python and a folder on the root of your C: drive.
## Environment
This is a command line build that moves your spreadsheet from the source and adds it to the data model on Snowflake cloud database.
Once the Excel files are loaded in as JSON format, the data is then moved to tables and organised for reporting.


## Prerequisites and Setup steps
1. Create a folder on the Root of C: drive and place the files in the test folder there 
2. The file can be executed using __main__ on main.py
3. The program will move you through a series of question mainly regarding logging in .
4. User logins can be found on the main.py page in the list: users_and_password_list 
5. Excel files to be added to the C:/XL/ folder to the root are:
   QA_Project_Prem.xls
   QA_Project_Prem_B.xls 

## Credentials for accessing and reviewing Snowflake
1. Snowflake environment log in page: https://oa67150.uk-south.azure.snowflakecomputing.com/oauth/authorize?client_id=o3T7BHUORVCe1wgcU23V3m8DnzIQxw%3D%3D&display=popup&redirect_uri=https%3A%2F%2Fapps-api.c1.uksouth.azure.app.snowflake.com%2Fcomplete-oauth%2Fsnowflake&response_type=code&scope=refresh_token&state=%7B%22browserUrl%22%3A%22https%3A%2F%2Fapp.snowflake.com%2Fuk-south.azure%2Foa67150%2Fw3cLHL9Vhl8z%23query%22%2C%22csrf%22%3A%22030baf09%22%2C%22isSecondaryUser%22%3Afalse%2C%22oauthNonce%22%3A%22Ax30TiKFNhq%22%2C%22url%22%3A%22https%3A%2F%2Foa67150.uk-south.azure.snowflakecomputing.com%22%2C%22windowId%22%3A%2201bb5531-a7a3-4052-8b0c-520031124158%22%7D
2. User name: PATRICKQAPROJECT
3. Password: 5n0VVF1Ak3
