from app.tool.base import BaseTool
from typing import Any
from app.tool.metabase_tools.client import MetabaseClient 

class MetabaseCreateCardTool(BaseTool):
    name: str = "create_metabase_card"
    description: str = "可以对在 Metabase 中的一个数据库中的数据创建新的卡片，卡片内容是一个sql语句"

    parameters: dict = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "卡片名称，一般是简略描述 SQL 查询作用，例如：获取 account 表的所有内容"
        },
        "dataset_query": {
            "type": "object",
            "description": "查询信息，包括 database(数据库 id)、type(一般为 native)、native: {template-tags: {}, query: SQL 语句}",
            "properties": {
                "database": {
                    "type": "integer",
                    "description": "目标数据库的 ID，可通过查询 /api/database 获取"
                },
                "type": {
                    "type": "string",
                    "enum": ["native"],
                    "description": "查询类型，通常为 native（原生 SQL）"
                },
                "native": {
                    "type": "object",
                    "description": "包含 SQL 查询和参数设置",
                    "properties": {
                        "template-tags": {
                            "type": "object",
                            "description": "可选，SQL 中的参数设置，通常为空即可",
                            "default": {}
                        },
                        "query": {
                            "type": "string",
                            "description": "SQL 查询语句，例如 SELECT * FROM ACCOUNT"
                        }
                    },
                    "required": ["query"]
                }
            },
            "required": ["database", "type", "native"]
        },
        "display": {
            "type": "string",
            "description": "卡片展示方式，例如 table（表格）、bar（柱状图）、line（折线图）、area（面积图）、pie（饼图）、scalar（单值）、object（对象）等",
            "enum": ["table", "bar", "line", "area", "pie", "scalar", "object"]
        },
        "visualization_settings": {
            "type": "object",
            "description": "可视化设置，决定哪些字段显示(如果不知道有哪些字段，可以使用mysql_execute工具)，格式通常为：{\"table.columns\": [{\"name\": \"字段名\", \"enabled\": true/false}, ...]}",
            "example": {
                "table.columns": [
                    {"name": "ACCOUNT_ID", "enabled": True},
                    {"name": "USER_NAME", "enabled": True},
                    {"name": "EMAIL", "enabled": True},
                    {"name": "PASSWORD", "enabled": False}
                ]
            }
        }
    },
    "required": ["name", "dataset_query", "display", "visualization_settings"]
}


    async def execute(self, name: str, dataset_query: dict, display: str,visualization_settings:dict) -> Any:
        try:
            client = MetabaseClient()
            client.login()
            res = client.create_card(name, dataset_query, display, visualization_settings)
            if res.status_code != 200:
                return {"error": "添加卡片失败", "status_code": res.status_code, "msg": res.text}
            else:
                return {"success": "添加卡片成功", "data": res.json()}
        except Exception as e:
            return {"error": str(e)}
        