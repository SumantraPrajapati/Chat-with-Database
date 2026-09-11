import sqlite3
import os
from google.adk.tools import FunctionTool

# database_assistant/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# talk with database/
PROJECT_DIR = os.path.dirname(BASE_DIR)

# talk with database/database/
DATABASE_DIR = os.path.join(PROJECT_DIR, "database")


db_file_name = None

for file in os.listdir(DATABASE_DIR):
    if file.lower().endswith(".db"):
        db_file_name = file
        break


if db_file_name:
    DB_NAME = os.path.join(DATABASE_DIR, db_file_name)
else:
    DB_NAME = None

def query_database(sql: str) -> dict:

    sql_clean = sql.strip().lower()
    
    if not sql_clean.startswith("select"):
        return{
            "success": False,
            "error" : "Only SELECT queries are allowed"
        }
    blocked = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "replace",
        "attach",
        "detach"
    ]
    
    for keyword in blocked:
        if keyword in sql_clean:
            return {
                "success": False,
                "error": f"Operation '{keyword}' is not allowed"
            }
            
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        
        columns = [
            description[0]
            for description in cursor.description
        ]
        conn.close()
        
        result = [
            dict(zip(columns , row))
            for row in rows
        ]
        
        return {
            "success":True,
            "data":result
        }
    except  Exception as e:
        return {
            "sucess": False,
            "error" : str(e)
        }
        
        
database_tool = FunctionTool(
    func = query_database
)
