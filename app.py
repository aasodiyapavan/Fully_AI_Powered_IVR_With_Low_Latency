from flask import Flask, request, send_file, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from google_tts import generate_tts
from twilio_helper import twilio_make_call
import uuid
import os

app = Flask(__name__)

@app.route("/initiate_call", methods=["GET"])
def initiate_call():
    number = request.args.get("number")
    text = request.args.get("text", "Hello! This is your AI caller speaking.")
    
    mp3_file = f"static/audio/{uuid.uuid4()}.mp3"
    generate_tts(text, mp3_file)

    twilio_make_call(number, mp3_file)
    return {"status": "Call initiated"}

@app.route("/play_audio", methods=["GET"])
def play_audio():
    audio = request.args.get("file")
    return send_file(audio, mimetype="audio/mpeg")

@app.route("/call_webhook", methods=["POST"])
def call_webhook():
    user_speech = request.values.get("SpeechResult", "")
    
    # Generate next reply using ChatGPT
    from openai import OpenAI
    client = OpenAI()
    bot_reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI phone assistant."},
            {"role": "user", "content": user_speech}
        ]
    ).choices[0].message["content"]

    mp3_file = f"static/audio/{uuid.uuid4()}.mp3"
    generate_tts(bot_reply, mp3_file)

    vr = VoiceResponse()
    vr.play(f"{request.url_root}play_audio?file={mp3_file}")
    vr.record(max_length=10, timeout=3, transcribe=False, action="/call_webhook")
    return Response(str(vr), mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
