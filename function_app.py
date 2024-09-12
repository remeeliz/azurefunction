import azure.functions as func
import logging
import pyodbc
import os
import json

server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")
#driver = '{ODBC Driver 17 for SQL Server}'

driver = '{ODBC Driver 18 for SQL Server}'
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="remeehttp")
def remeehttp(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Establish connection to SQL Server
        #conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Authentication=ActiveDirectoryMsi')
        cursor = conn.cursor()
        
        # Example query
        cursor.execute("select * from sys.objects for json auto")
        rows = cursor.fetchall()
        result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            
        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")
    
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
