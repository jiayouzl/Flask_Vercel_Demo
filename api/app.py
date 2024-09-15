# -*- coding: UTF-8 -*-

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


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


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5001, debug=True)
