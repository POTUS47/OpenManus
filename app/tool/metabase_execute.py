import requests
from app.tool.base import BaseTool
from app.tool.metabase_client import MetabaseClient

class MetabaseCardQueryTool(BaseTool):
    name: str = "query_metabase_card"
    description: str = "根据卡片 ID 执行该卡片内容操作 Metabase 中的数据并获得结果"

    parameters: dict = {
        "type": "object",
        "properties": {
            "base_url": {"type": "string", "description": "Metabase 的基础 URL"},
            "username": {"type": "string", "description": "用户名"},
            "password": {"type": "string", "description": "密码"},
            "card_id": {"type": "integer", "description": "卡片 ID"}
        },
        "required": ["base_url", "username", "password", "card_id"]
    }

    async def execute(self, base_url: str, username: str, password: str, card_id: int) -> Any:
        try:
            client = MetabaseClient(base_url, username, password)
            client.login()
            res = client.post(f"/api/card/pivot/{card_id}/query")
            data = res.json()

            if "data" in data and "rows" in data["data"]:
                rows = data["data"]["rows"]
                cols = data["data"].get("cols", [])
                return [
                    {cols[i]["display_name"]: row[i] for i in range(len(row))}
                    for row in rows
                ]
            else:
                return {"error": "数据结构异常", "raw": data}
        except Exception as e:
            return {"error": str(e)}
