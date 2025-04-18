from app.tool.base import BaseTool
from typing import Any, Dict
from app.tool.metabase_tools.client import MetabaseClient

class MetabaseAddDatabaseTool(BaseTool):
    name: str = "metabase_add_database"
    description: str = "将某ip的数据库（可为远程服务器，可为本地，若是本地，host部分localhost要改成host.docker.internal）添加到 Metabase中作为新数据库,随后会获得新数据库的id"

    parameters: dict = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "数据库显示名称"},
            "engine": {"type": "string", "description": "数据库类型，如 mysql"},
            "details": {"type": "object", "description": "连接信息，包括 host、port、user、password、dbname"}
        },
        "required": ["name", "engine", "details"]
    }

    async def execute(self, name: str, engine: str, details: Dict[str, Any]) -> Any:
        try:
            client = MetabaseClient()
            client.login()
            res = client.add_database(name, engine, details)
            return res
        except Exception as e:
            return {"error": str(e)}

