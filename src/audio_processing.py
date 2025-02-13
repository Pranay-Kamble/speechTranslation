import wave
import numpy as np
import noisereduce as nr

def process_with_noisereduce(input_file, output_file):
    # Open the input WAV file
    print("Ok Running")
    with wave.open(input_file, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)

    # Assume noise sample is from the first 1 second of the audio
    noise_sample = audio_data[:params.framerate]  # 1-second noise sample

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, y_noise=noise_sample, sr=params.framerate)

    # Save the processed audio
    with wave.open(output_file, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(reduced_noise.astype(np.int16).tobytes())

    print(f"Processed audio saved to {output_file}")

# Example usage
input_audio = "./data/harvard.wav"  # Replace with your input file path
output_audio = "./data/cleaned_audio.wav"  # Replace with desired output file path
process_with_noisereduce(input_audio, output_audio)
