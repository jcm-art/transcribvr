#Modules under test

#Dependencies
import os

def test_client_single_mp3_audio_file():
    import os
    os.system("python3 transcription_client.py tests/resources/audio.mp3")


