#Modules under test
from transcribvr.transcription_manager import TranscriptionManager

#Dependencies
import os

def test_buffer_filepath():
    tm = TranscriptionManager()
    assert tm.get_buffer_filepath()=="./audio_input/"

def test_readiness():
    tm = TranscriptionManager()
    assert tm.check_if_ready_for_transcription()

def test_single_m4a_audio_file():
    test_file = "audio.m4a"
    print(os.getcwd())
    test_file_path = os.path.join("tests/resources/",test_file)
    print(test_file_path)
    # 
    tm = TranscriptionManager()
    tm.assign_transcription(test_file_path)

def test_single_mp3_audio_file():
    test_file = "audio.mp3"
    test_file_path = os.path.join("tests/resources/",test_file)

    tm = TranscriptionManager()
    tm.assign_transcription(test_file_path)


