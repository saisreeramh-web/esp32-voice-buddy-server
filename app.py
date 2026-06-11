from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_KEY = "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"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data["text"]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = r.json()

    answer = result["choices"][0]["message"]["content"]

    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
