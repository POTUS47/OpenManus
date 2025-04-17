import mysql.connector
from typing import Any
from app.tool.base import BaseTool

class MySQLExecuteTool(BaseTool):
    name: str = "query_mysql"
    description: str = "查询本地 MySQL 数据库内容"

    parameters: dict = {
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "数据库地址"},
            "user": {"type": "string", "description": "用户名"},
            "password": {"type": "string", "description": "密码"},
            "database": {"type": "string", "description": "数据库名"},
            "query": {"type": "string", "description": "SQL 查询语句"}
        },
        "required": ["host", "user", "password", "database", "query"]
    }

    async def execute(self, host: str, user: str, password: str, database: str, query: str) -> Any:
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()