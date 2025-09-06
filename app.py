from flask import Flask, request, jsonify
import io, wave, os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("VOICE_BUDDY_API_KEY")

@app.route("/")
def home():
    return "✅ Voice Buddy Server is online!"

@app.route("/upload", methods=["POST"])
def upload_audio():
    try:
        raw = request.data

        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(raw)
        wav_io.seek(0)

        audio_file = wav_io
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        user_text = transcription["text"]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200
        )
        ai_reply = completion.choices[0].message["content"].strip()

        return jsonify({"transcript": user_text, "response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
