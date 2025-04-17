# app/tool/metabase/client.py
import requests

class MetabaseClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session_id = None
        self.headers = {}

    def login(self):
        resp = requests.post(
            f"{self.base_url}/api/session",
            json={"username": self.username, "password": self.password}
        )
        resp.raise_for_status()
        self.session_id = resp.json()["id"]
        self.headers = {"X-Metabase-Session": self.session_id}

    def get(self, path: str):
        return requests.get(f"{self.base_url}{path}", headers=self.headers)

    def post(self, path: str, json=None):
        return requests.post(f"{self.base_url}{path}", json=json, headers=self.headers)

    def delete(self, path: str):
        return requests.delete(f"{self.base_url}{path}", headers=self.headers)

    def put(self, path: str, json=None):
        return requests.put(f"{self.base_url}{path}", json=json, headers=self.headers)
