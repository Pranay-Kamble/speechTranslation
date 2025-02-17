from gtts import gTTS # Requires Internet
import os

# Function to convert text to speech and save it locally
def generate_audio_from_file(file_path, language='hi', output_filename='data/output.mp3'):
    try:
        # Read text from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_filename)
        print(f"Audio saved as {output_filename}")

    except Exception as e:
        print(f"Error reading file or generating audio: {e}")

# Function to play the generated audio
def play_audio(filename):
    # For Linux: os.system(f"xdg-open {filename}")
    os.system(f"open {filename}")

# Sample usage


# Play the generated audio file (optional)
# play_audio(output_audio_filename)
