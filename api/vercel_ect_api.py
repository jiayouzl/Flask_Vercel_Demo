# -*- coding: UTF-8 -*-

# 基于Vercel Edge Config API的Python3客户端
# 1. 创建https://vercel.com/jiayouzls-projects/~/stores 创建一个Edge Config(然后需要再Projects中关联项目)
# 2. 创建https://vercel.com/account/settings/tokens 创建一个全局的Token
# 3. KV_REST_API_TOKEN = 全局Token
# 4. VERCEL_CONFIG_ID = Edge Config的ID 在刚创建的Edge Config的URL中可以找到(名称为：ID)
# 5. 在https://vercel.com/jiayouzls-projects/flask-vercel-demo/settings/environment-variables 中设置好环境变量

import os

import httpx
from dotenv import load_dotenv


class VercelEdgeConfig:
    def __init__(self):
        # load_dotenv()  # 从.env文件中加载环境变量(本地测试时使用)
        self.base_url = "https://api.vercel.com/v1/edge-config"
        self.token = os.environ.get("KV_REST_API_TOKEN")
        self.config_id = os.environ.get("VERCEL_CONFIG_ID")

        if not self.token or not self.config_id:
            raise ValueError("KV_REST_API_TOKEN 和 VERCEL_CONFIG_ID 必须要在VERCEL环境变量中设置")

    async def set(self, key, value):
        url = f"{self.base_url}/{self.config_id}/items"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {"items": [{"operation": "upsert", "key": key, "value": value}]}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"Error setting key '{key}': {response.status_code}, {response.text}")
            return response.status_code == 200

    async def get(self, key):
        url = f"{self.base_url}/{self.config_id}/items"
        headers = {"Authorization": f"Bearer {self.token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            # print(f"Response status: {response.status_code}")
            # print(f"Response content: {response.text}")

            if response.status_code == 200:
                items = response.json()  # 直接获取返回的列表
                if isinstance(items, list):
                    for item in items:
                        if item["key"] == key:
                            return item["value"]
                print(f"Key '{key}' not found")
            else:
                print(f"Error: {response.status_code}, {response.text}")
            return None

    async def delete(self, key):
        url = f"{self.base_url}/{self.config_id}/items"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {"items": [{"operation": "delete", "key": key}]}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
            return response.status_code == 200

    async def list_items(self):
        url = f"{self.base_url}/{self.config_id}/items"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            print(f"List items response: {response.status_code}, {response.text}")
            if response.status_code == 200:
                return response.json()
            return None
