import os
import base64
import requests

def gcloud_tts(path, text, lang='sv-SE', name='sv-SE-Wavenet-E'):
    if os.path.exists(path):
        return

    assert (key := os.getenv("GCLOUD_TTS_API_KEY")) != None,\
        "Set GCLOUD_TTS_API_KEY or else ..."

    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    payload =  {
        "audioConfig": {
            # https://cloud.google.com/text-to-speech/docs/reference/rest/v1/AudioConfig
            "audioEncoding": "MP3",
            "pitch": 0,
            "speakingRate": 0.9,
        },
        "input": {
            "ssml": f"<speak>{text}</speak>"
        },
        "voice": {
            "languageCode": lang,
            "name": name,
        }
    }
    r = requests.post(f"{url}?key={key}", headers={}, json=payload)
    r.raise_for_status()
    data = r.json()
    encoded = data['audioContent']
    audio = base64.b64decode(encoded)
    with open(path, 'wb') as response_output:
        response_output.write(audio)
