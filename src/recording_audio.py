"""
This file is supposed to only record the audio from the user
After recording the audio, it is stored in speechTranslation/src/audioData/raw_audio.wav
"""

import os
from pynput import keyboard
import pyaudio
import wave
import threading

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
DIRECTORY = "data/"
FILENAME = "raw_audio.wav"

recording = False
exit_program = False
audio_frames = []
p = pyaudio.PyAudio()

# Ensure the directory exists
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

def record_audio():
    global recording, audio_frames
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording started...")
    while recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frames.append(data)
    stream.stop_stream()
    stream.close()
    print("Recording stopped.")

def save_audio():
    file_path = os.path.join(DIRECTORY, FILENAME)  # Combine directory and file name
    print(f"Saving audio to file: {file_path}")
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    print(f"Audio saved as {file_path}")

def toggle_recording(key):
    global recording, audio_frames, exit_program
    try:
        if key.char == 'r':  # Toggle recording
            if not recording:
                # Start recording
                audio_frames = []  # Reset audio frames
                recording = True
                threading.Thread(target=record_audio).start()
            else:
                # Stop recording
                recording = False
                save_audio()
        elif key.char == 'q':  # Exit the program
            print("Exiting program...")
            exit_program = True
            if recording:  # Stop recording if active
                recording = False
    except AttributeError:
        pass  # Handle special keys
