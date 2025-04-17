import mysql.connector
from typing import Any
from app.tool.base import BaseTool

class MySQLExecuteTool(BaseTool):
    name: str = "query_mysql"
    # 描述很重要，大模型根据描述判断什么时候调用工具
    description: str = "该工具可以用来连接 MySQL 数据库，包括本地数据库和远程数据库"

    parameters: dict = {
        "type": "object",
        "properties": {
            "host": {"type": "string",
                     "description": "数据库地址",
                     "default": "localhost"},
            "user": {"type": "string",
                     "description": "用户名",
                     "default": "root"},
            "password": {"type": "string",
                         "description": "密码",
                         "default": "mysql"},
            "database": {"type": "string",
                         "description": "数据库名",
                         "default": "openmanus"},
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