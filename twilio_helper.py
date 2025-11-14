from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_AUTH"
twilio_number = "YOUR_TWILIO_NUMBER"

client = Client(account_sid, auth_token)

def twilio_make_call(to_number, mp3_file):
    url = f"https://YOUR_SERVER_DOMAIN/play_audio?file={mp3_file}"

    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url=url
    )
    return call.sid
