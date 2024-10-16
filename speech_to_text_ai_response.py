import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import sounddevice as sd
import numpy as np
import language_tool_python
from gtts import gTTS
from playsound import playsound
import google.generativeai as genai
import textwrap
import re
from dotenv import load_dotenv
import os

modelo_wav2vec2 = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")
procesador_wav2vec2 = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")

tool = language_tool_python.LanguageTool('es')

def transcribir_audio_microfono():
    try:
        fs = 16000
        duracion = 5

        print("Grabando audio...")

        audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype="float32")
        sd.wait()

        print("Grabación finalizada.")

        audio = np.squeeze(audio)
        input_values = procesador_wav2vec2(audio, sampling_rate=fs, return_tensors="pt", padding=True)

        with torch.no_grad():
            logits = modelo_wav2vec2(input_values.input_values).logits

        transcripcion = procesador_wav2vec2.batch_decode(logits.argmax(dim=-1))[0]
        print("Sin corregir: " + transcripcion)

        transcripcion_corregida = tool.correct(transcripcion)
        print("\nCorregida: " + transcripcion_corregida)

        return transcripcion_corregida
    
    except Exception as e:
        print(f"Se produjo un error al transcribir el audio desde el micrófono: {e}")
        return None

load_dotenv()
genai_api_key = os.getenv("GEMINI_APIKEY")

genai.configure(api_key = genai_api_key)
model = genai.GenerativeModel('gemini-pro')

texto_transcrito = transcribir_audio_microfono()

PROMPT = texto_transcrito
response1 = model.generate_content(PROMPT)
max_chars = 500
texto1 = textwrap.shorten(response1.text, max_chars)

print("Con *: " + texto1)

texto_limpio = re.sub(r"\*", "", texto1)
texto_limpio = texto_limpio.strip()

print("\nSin *: " + texto_limpio)

tts = gTTS(text=texto_limpio, lang="es")
filename = "audio_respuesta.mp3"
tts.save(filename)

playsound(filename)