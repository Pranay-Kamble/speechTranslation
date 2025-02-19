from src import *

"""
#Assumptions Made:
1) Push to talk will be implemented when integrating with Raspberry Pi as holding the button on keyboard and recording is creating errors 
2) For now, I have disabled the noise cancellation part as it is also reducing the details from the audio
3) Only English to Hindi has been taken care of for now
4) Outputting the type of modes, input and output languages on the LED display will be done later
5) We need to work on improving the accuracy of noise input
6) Used gTTS for conversion of text into audio as no other offline model could be found
   There is pyttsx3 which uses espeak engine, it is giving very poor output and not suitable for hearing (noisy and robotic voice, almost shit)
"""

MODEL_PATH = "../models/vosk/vosk-model-small-en-in-0.4"
INPUT_AUDIO = "data/raw_audio.wav"  # Replace with the path to your audio file #

# Recording the audio
listener = keyboard.Listener(on_press=toggle_recording)
listener.start()

print("Press 'r' to start/stop recording and 'q' to quit.")
# while not exit_program:
#     pass

exit_program_event.wait()

listener.stop()
print("Recording the audio phase has been completed\n\n")

# Reducing noise from the Audio
# input_audio = "./data/raw_audio.wav"  # Replace with your input file path
# output_audio = "./data/cleaned_audio.wav"  # Replace with desired output file path
# process_with_noisereduce(input_audio, output_audio)
# print("Processing the audio phase has been completed\n\n")

# Speech to text conversion

try:
    # Step 1: Verify and convert audio format if necessary
    if not check_audio_format(INPUT_AUDIO):
        print("Audio format is incompatible. Converting...")
        convert_audio_format(INPUT_AUDIO, "data/converted_audio.wav")
        audio_path = "data/converted_audio.wav"
    else:
        audio_path = INPUT_AUDIO

    # Step 2: Process the full audio file
    text_output = process_full_audio(audio_path)
    print("Recognized Text:")
    print(text_output)

    # Step 3: Save the text output to a file
    with open("data/recognized_text.txt", "w", encoding="utf-8") as f:
        f.write(text_output)
    print("Text saved to recognized_text.txt")

except Exception as e:
    print(f"Error: {e}")

print("Conversion of speech to text has been completed\n\n")

# Text Translation to hindi

try:
    # File paths
    input_text_path = "data/recognized_text.txt"
    output_text_path = "data/translated_text.txt"

    # Read input text
    with open(input_text_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    # Setup translation model
    setup_translation_model(from_lang="en", to_lang="hi", model_dir="./models/argos/translate")

    # Translate the text
    translated_text = translate_text(input_text, from_lang="en", to_lang="hi")
    print("Translated Text:")
    print(translated_text)

    # Save translated text to a file
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(translated_text)
    print(f"Translated text saved to {output_text_path}")

except Exception as e:
    print(f"Error: {e}")

print("Translation of the text is completed\n\n")
# Text to audio conversion

file_path = "data/translated_text.txt"  # Specify the path to your file
output_audio_filename = "data/output.wav"  # Specify the desired output file name

# Generate the audio from the text file
generate_audio_from_file(file_path, language='hi', output_filename=output_audio_filename)

print("Generating the new audio phase has been completed\n\n")