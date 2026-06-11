from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "YOUR_KEY"

@app.route("/ask", methods=["POST"])
def ask():

    data = request.json
    prompt = data["text"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents":[
            {
                "parts":[
                    {
                        "text":prompt
                    }
                ]
            }
        ]
    }

    r = requests.post(url,json=payload)

    result = r.json()

    answer = result["candidates"][0]["content"]["parts"][0]["text"]

    return jsonify({"reply":answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
