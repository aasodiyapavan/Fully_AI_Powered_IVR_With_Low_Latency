import requests

def generate_tts(text, output_file):
    url = "https://translate.google.com/translate_tts"
    params = {
        "ie": "UTF-8",
        "q": text,
        "tl": "en",
        "client": "tw-ob"
    }

    response = requests.get(url, params=params, headers={
        "User-Agent": "Mozilla/5.0"
    })

    with open(output_file, "wb") as f:
        f.write(response.content)
