from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

ZHIPU_KEY = os.getenv("ZHIPU_API_KEY")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("content", "")
        if not user_msg:
            return jsonify({"err": "内容不能为空"}), 400

        payload = {
            "model": "glm-4-flash",
            "messages": [{"role": "user", "content": user_msg}]
        }
        headers = {
            "Authorization": f"Bearer {ZHIPU_KEY}",
            "Content-Type": "application/json"
        }
        res = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"err": str(e)}), 500

# 不要写 app.run 端口那一段！Vercel会自动处理

