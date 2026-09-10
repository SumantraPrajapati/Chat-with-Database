import sqlite3
from google.adk.tools import FunctionTool
import os

target_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database File")

db_file_name = None
for entry in os.listdir("Database File"):
    if entry.endswith(".db"):
        db_file_name = entry
        break  

DB_NAME = db_file_name

def query_database(sql: str) -> dict:
    """
    Execute a READ-ONLY SQL query against the company database.
    Only SELECT statements are allowed.
    
    """
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
            dict(zip(columns , rows))
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
