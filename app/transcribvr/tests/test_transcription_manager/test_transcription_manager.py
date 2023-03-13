#Modules under test
from transcribvr.transcription_manager import TranscriptionManager

#Dependencies
import os



def test_buffer_filepath():
    adm = TranscriptionManager()
    assert adm.get_buffer_filepath()=="./audio_input/"

def test_readiness():
    adm = TranscriptionManager()
    assert adm.check_if_ready_for_transcription()

def test_single_m4a_audio_file():
    test_file = "audio.m4a"
    test_file_path = os.path.abspath("tests/resources/"+test_file)

    adm = TranscriptionManager()
    adm.assign_transcription(test_file_path)

def test_single_mp3_audio_file():
    test_file = "audio.mp3"
    test_file_path = os.path.abspath("tests/resources/"+test_file)

    adm = TranscriptionManager()
    adm.assign_transcription(test_file_path)


