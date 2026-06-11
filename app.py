from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("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")

@app.route("/")
def home():
    return "ESP32 Voice Buddy Server Running!"

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    prompt = data["text"]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 200
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({
            "error": response.text
        }), response.status_code

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
