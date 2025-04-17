from app.tool.base import BaseTool
from typing import Any
from app.tool.metabase_tools.client import MetabaseClient  # 分离 Metabase 客户端

class MetabaseCardQueryTool(BaseTool):
    name: str = "metabase_query_card"
    description: str = "可以连接到metabase并执行 Metabase 卡片并获取数据"

    parameters: dict = {
        "type": "object",
        "properties": {
            "card_id": {"type": "integer", "description": "Metabase 卡片的 ID"},
        },
        "required": ["card_id"]
    }

    async def execute(self, card_id: int) -> Any:
        try:
            client = MetabaseClient()
            client.login()
            return client.get_card_data(card_id)
        except Exception as e:
            return {"error": str(e)}
