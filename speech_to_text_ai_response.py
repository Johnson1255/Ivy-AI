"""
Speech-to-Text AI Response System

This module implements a system that transcribes speech from a microphone,
corrects the transcription, generates an AI response, and converts the
response back to speech.

The system uses the following main components:
- Wav2Vec2 for speech recognition
- LanguageTool for text correction
- Gemini AI for content generation
- gTTS for text-to-speech conversion

Requirements:
- Python 3.12.2+
- See requirements.txt for necessary packages
"""

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

# Initialize Wav2Vec2 model and processor
modelo_wav2vec2 = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")
procesador_wav2vec2 = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")

# Initialize LanguageTool for Spanish
tool = language_tool_python.LanguageTool('es')

def transcribir_audio_microfono():
    """
    Record audio from the microphone, transcribe it using Wav2Vec2,
    and correct the transcription using LanguageTool.

    Returns:
    str: The corrected transcription of the recorded audio.
    None: If an error occurs during the process.
    """
    try:
        # Set up audio recording parameters
        fs = 16000  # Sample rate
        duracion = 5  # Recording duration in seconds

        print("Grabando audio...")
        # Record audio
        audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype="float32")
        sd.wait()
        print("Grabación finalizada.")

        # Prepare audio for transcription
        audio = np.squeeze(audio)
        input_values = procesador_wav2vec2(audio, sampling_rate=fs, return_tensors="pt", padding=True)

        # Transcribe audio
        with torch.no_grad():
            logits = modelo_wav2vec2(input_values.input_values).logits
        transcripcion = procesador_wav2vec2.batch_decode(logits.argmax(dim=-1))[0]
        print("Sin corregir: " + transcripcion)

        # Correct transcription
        transcripcion_corregida = tool.correct(transcripcion)
        print("\nCorregida: " + transcripcion_corregida)

        return transcripcion_corregida
    
    except Exception as e:
        print(f"Se produjo un error al transcribir el audio desde el micrófono: {e}")
        return None

# Load environment variables and configure Gemini AI
load_dotenv()
genai_api_key = os.getenv("GEMINI_APIKEY")

genai.configure(api_key = genai_api_key)
model = genai.GenerativeModel('gemini-pro')

# Main execution
if __name__ == "__main__":
    # Transcribe audio
    texto_transcrito = transcribir_audio_microfono()

    if texto_transcrito:
        # Generate AI response
        PROMPT = texto_transcrito
        response1 = model.generate_content(PROMPT)
        max_chars = 500
        texto1 = textwrap.shorten(response1.text, max_chars)

        print("Con *: " + texto1)

        # Clean up the generated text
        texto_limpio = re.sub(r"\*", "", texto1)
        texto_limpio = texto_limpio.strip()

        print("\nSin *: " + texto_limpio)

        # Convert text to speech
        tts = gTTS(text=texto_limpio, lang="es")
        filename = "audio_respuesta.mp3"
        tts.save(filename)

        # Play the generated audio
        playsound(filename)
    else:
        print("No se pudo procesar el audio. Por favor, intente de nuevo.")