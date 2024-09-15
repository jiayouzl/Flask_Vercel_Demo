# -*- coding: UTF-8 -*-

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


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5001, debug=True)
