import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import sounddevice as sd
import numpy as np
import language_tool_python

#Spanish Transformers
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
