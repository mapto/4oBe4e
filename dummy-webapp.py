#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import request, redirect, send_from_directory

static_path = "."

app = Flask(__name__, static_url_path="/.")


@app.route("/action_page.php")
def process():
    print(f"URL: {request.url}")
    print(f"== Headers ==\n{request.headers}\n")
    print(f"Method: {request.method}")
    print(f"Arguments: {request.args}")
    print(f"== Data ==\n{request.data}\n")
    # print(f"== JSON ==\n{request.json}\n")
    # print(f"Endpoint: {request.endpoint}")
    # print(f"Remote: {request.remote_addr}")
    # print(f"Browser: {request.user_agent}")
    return redirect("4oBe4e.html")


@app.route("/<path:path>")
def send_resource(path):
    print(path)
    return send_from_directory(static_path, path)


@app.route("/")
def root():
    print("root")
    return send_from_directory(static_path, "4oBe4e.html")


if __name__ == "__main__":
    app.run(debug=True)
