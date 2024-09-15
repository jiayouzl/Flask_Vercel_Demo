# -*- coding: UTF-8 -*-

import asyncio

import requests
from flask import Flask, jsonify, render_template, request

# 条件导入
try:
    from vercel_ect_api import VercelEdgeConfig
except ImportError:
    from api.vercel_ect_api import VercelEdgeConfig

app = Flask(__name__)
edge_config = VercelEdgeConfig()


# http://127.0.0.1:5001
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# http://127.0.0.1:5001/api
# http://127.0.0.1:5001/api?name=hello
@app.route("/api", methods=["GET"])
def api():
    if request.args.get("name") is None:
        return jsonify({"error": "no name"})
    return jsonify({"name": request.args.get("name")})


# http://127.0.0.1:5001/get_ip_parse
@app.route("/get_ip_parse", methods=["GET"])
def get_ip_parse():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    }

    params = {
        "json": "true",
    }

    response = requests.get("http://whois.pconline.com.cn/ipJson.jsp", params=params, headers=headers, verify=False).json()
    return jsonify({"ip": response["ip"], "city": response["city"], "addr": response["addr"]})


# http://127.0.0.1:5001/set/name/zhanglei
@app.route("/set/<key>/<value>")
def set_value(key, value):
    result = asyncio.run(edge_config.set(key, value))
    return "Success" if result else "Failed"


# http://127.0.0.1:5001/get/name
@app.route("/get/<key>")
def get_value(key):
    value = asyncio.run(edge_config.get(key))
    if value is None:
        return f"Key '{key}' not found", 404
    return str(value)


# http://127.0.0.1:5001/delete/greeting
@app.route("/delete/<key>")
def delete_value(key):
    result = asyncio.run(edge_config.delete(key))
    return "Success" if result else "Failed"


# http://127.0.0.1:5001/list_items
@app.route("/list_items")
def list_items():
    items = asyncio.run(edge_config.list_items())
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
