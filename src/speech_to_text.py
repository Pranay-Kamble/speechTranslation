import wave
import numpy as np
import vosk
import json
import os

# Vosk model path
MODEL_PATH = "models/vosk/vosk-model-small-en-us-0.15"
INPUT_AUDIO = "data/harvard.wav"  # Replace with the path to your audio file


def check_audio_format(audio_path):
    """Check if audio format meets Vosk's requirements."""
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            return False
    return True


def convert_audio_format(audio_path, output_path):
    """Convert audio to WAV format with required specifications."""
    with wave.open(audio_path, "rb") as wf:
        # Read original audio parameters
        channels = wf.getnchannels()
        rate = wf.getframerate()
        width = wf.getsampwidth()

        # Convert audio to mono and 16-bit, 16kHz
        with wave.open(output_path, "wb") as out_wf:
            out_wf.setnchannels(1)  # Mono
            out_wf.setsampwidth(2)  # 16-bit
            out_wf.setframerate(16000)  # 16kHz

            # Read frames and convert as needed
            frames = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)

            if channels > 1:
                audio_data = audio_data[::channels]  # Downmix to mono

            if rate != 16000:
                # Resample if necessary (use scipy or librosa for better resampling)
                import scipy.signal
                audio_data = scipy.signal.resample(audio_data, int(len(audio_data) * 16000 / rate))

            out_wf.writeframes(audio_data.astype(np.int16).tobytes())


def process_full_audio(audio_path):
    """Process the entire audio file and return transcribed text."""
    # Load Vosk model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Vosk model not found at {MODEL_PATH}. Please download and set up the model.")
    model = vosk.Model(MODEL_PATH)

    # Open the audio file
    with wave.open(audio_path, "rb") as wf:
        recognizer = vosk.KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        # Process the entire audio
        frames = wf.readframes(wf.getnframes())
        if len(frames) == 0:
            raise ValueError("The audio file is empty or unreadable.")

        if recognizer.AcceptWaveform(frames):
            result = json.loads(recognizer.Result())
            return result.get("text", "")
        else:
            final_result = json.loads(recognizer.FinalResult())
            return final_result.get("text", "")

