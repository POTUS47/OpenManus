# from app.tool.base import BaseTool
# from typing import ClassVar
# import requests

# class MetabaseToolBase(BaseTool):
#     base_url: ClassVar[str] = "http://127.0.0.1:3000"
#     username: ClassVar[str] = "pan332022@163.com"
#     password: ClassVar[str] = "3359433P"
#     session = None

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         if not MetabaseToolBase.session:
#             MetabaseToolBase.session = requests.Session()
#             token = MetabaseToolBase.session.post(
#                 f"{self.base_url}/api/session", json={
#                     "username": self.username,
#                     "password": self.password
#                 }
#             ).json()["id"]
#             MetabaseToolBase.session.headers.update({"X-Metabase-Session": token})

#     def get(self, path, **kwargs):
#         return self.session.get(f"{self.base_url}{path}", **kwargs)

#     def post(self, path, **kwargs):
#         return self.session.post(f"{self.base_url}{path}", **kwargs)
