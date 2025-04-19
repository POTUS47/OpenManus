import requests
from pathlib import Path
import yaml

class MetabaseClient:
    def __init__(self):
        with open(Path(__file__).parent / "config.yaml", "r") as f:
            conf = yaml.safe_load(f)
        self.base_url = "http://127.0.0.1:3000"
        self.username = conf["ClientUser"]["username"]
        self.password = conf["ClientUser"]["password"]
        self.session_id = None

    def login(self):
        response = requests.post(
            f"{self.base_url}/api/session",
            json={"username": self.username, "password": self.password}
        )
        response.raise_for_status()
        self.session_id = response.json()["id"]

    def _headers(self):
        if not self.session_id:
            raise RuntimeError("Must login before making authenticated requests.")
        return {"X-Metabase-Session": self.session_id}

    def post(self, endpoint: str, data: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response

    def get_card_data(self, card_id: int):
        response = self.post(f"/api/card/pivot/{card_id}/query")
        data = response.json()

        if "data" in data and "rows" in data["data"]:
            rows = data["data"]["rows"]
            cols = data["data"].get("cols", [])
            return [
                {cols[i]["display_name"]: row[i] for i in range(len(row))}
                for row in rows
            ]
        else:
            return {"error": "数据结构异常", "raw": data}

    def create_card(self, name: str, dataset_query: dict, visualization_settings: dict, display: str = "table"):
        payload={
            "visualization_settings": {},
            "dataset_query": dataset_query,
            "name": name,
            "result_metadata": [],
            "collection_id": 5,
            "type": "question",
            "display": "table",
            "parameters": [],
        }
        response = requests.post("http://127.0.0.1:3000/api/card/",json=payload,headers=self._headers())
        #response.raise_for_status()
        return response


    def add_database(self, name: str, engine: str, details: dict):
        payload = {
            "name": name,
            "engine": engine,
            "details": details,
            "is_full_sync": True,
            "connection_source": "admin",
            "auto_run_queries": True,
            "schedules": {
                "cache_field_values": {
                    "schedule_day": "sun",
                    "schedule_frame": "first",
                    "schedule_hour": 1,
                    "schedule_minute": 1,
                    "schedule_type": "hourly"
                },
                "metadata_sync": {
                    "schedule_day": "sun",
                    "schedule_frame": "first",
                    "schedule_hour": 1,
                    "schedule_minute": 1,
                    "schedule_type": "hourly"
                }
            }
        }
        response = requests.post(
            f"{self.base_url}/api/database",
            json=payload,
            headers=self._headers()
        )
        response.raise_for_status()
        database_id=self.get_database_id_by_name(name)
        if database_id:
            return {"success": "数据库添加成功！", "database_id": database_id}
        else:
            return {"error": "数据库添加失败，未能获取数据库ID"}

    def get_database_id_by_name(self,name):
        response = requests.get(f"{self.base_url}/api/database", headers=self._headers())
        #response.raise_for_status()  # 如果请求失败会抛出异常
        databases = response.json().get("data", [])

        for db in databases:
            if db.get("name") == name:
                return db.get("id")
        return None  # 没有找到目标数据库
