import requests
from os import getenv


class ZeroTierAPI:
    def __init__(self, api_token: str, base_url: str = "https://my.zerotier.com/api/"):
        self.token = api_token
        if self.token is None:
            raise Exception("ZT_TOKEN environment variable is required")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_node(self, network_id: str, node_id: str):
        """Get device information"""
        url = f"{self.base_url}network/{network_id}/member/{node_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()