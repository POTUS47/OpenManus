# from app.tool.base import BaseTool
# from app.tool.metabase_client import MetabaseClient
# from typing import Any

# class MetabaseCardQueryTool(BaseTool):
#     name: str = "query_metabase_card"
#     description: str = "该工具可以连接到metabase，并根据卡片 ID 执行该卡片内容操作 Metabase 中的数据并获得结果（结果为行列数据）"

#     parameters: dict = {
#         "type": "object",
#         "properties": {
#             "card_id": {"type": "integer", "description": "卡片 ID"},
#         },
#         "required": ["card_id"]
#     }

#     async def execute(self, card_id: int) -> Any:
#         try:
#             client = MetabaseClient(
#                 base_url="http://127.0.0.1:3000",
#                 username="pan332022@163.com",
#                 password="3359433P"
#             )
#             client.login()
#             res = client.post(f"/api/card/pivot/{card_id}/query")
#             data = res.json()

#             if "data" in data and "rows" in data["data"]:
#                 rows = data["data"]["rows"]
#                 cols = data["data"].get("cols", [])
#                 return [
#                     {cols[i]["display_name"]: row[i] for i in range(len(row))}
#                     for row in rows
#                 ]
#             else:
#                 return {"error": "数据结构异常", "raw": data}
#         except Exception as e:
#             return {"error": str(e)}
