#Modules under test

#Dependencies
import os
import pytest

output_filepath = "transcription_output"


@pytest.fixture
def clean_output():
    transcription_files = os.listdir(output_filepath)
    for file in transcription_files:
        print("removing file")
        os.remove(output_filepath + "/" + file)   

def test_client_single_mp3_audio_file(clean_output): 
    os.system("python3 transcription_client.py tests/resources/audio.mp3")
    assert os.path.isfile(output_filepath + "/" + "s0j0.txt")

def test_client_single_m4a_audio_file(clean_output):    
    syscommand = "python3 transcription_client.py tests/resources/audio.m4a"
    os.system(syscommand)
    assert os.path.isfile(output_filepath + "/" + "s0j0.txt")

@pytest.mark.parametrize("format",["aiff","flac","m4a","mp3","ogg","wav"])
def test_client_alt_audio_formats_from_libri(clean_output,format):    
    syscommand = "python3 transcription_client.py tests/resources/libri-test-clean-all-data-formats/libri-test-clean-sample0." + format
    os.system(syscommand)
    assert os.path.isfile(output_filepath + "/" + "s0j0.txt")

def test_two_audio_files(clean_output):    
    os.system("python3 transcription_client.py tests/resources/audio.m4a tests/resources/audio.mp3")

    transcription_filepath = output_filepath + "/" + "s0j0.txt"
    first_file=False
    second_file=False
    with open(transcription_filepath, 'r') as file:
        # read all content from a file using read()
        content = file.read()
        # check if string present or not
        if 's0j0f0' in content:
            first_file=True
        
        if 's0j0f1' in content:
            second_file=True
    
    assert first_file and second_file

def test_client_long_zip_file(clean_output):    
    syscommand = "python3 transcription_client.py tests/resources/zip_test.zip"
    os.system(syscommand)
    
    transcription_filepath = output_filepath + "/" + "s0j0.txt"
    first_file=False
    second_file=False
    with open(transcription_filepath, 'r') as file:
        # read all content from a file using read()
        content = file.read()
        # check if string present or not
        if 's0j0f0' in content:
            first_file=True
        
        if 's0j0f1' in content:
            second_file=True
    
    assert first_file and second_file
    
def test_long_audio_file(clean_output):    
    syscommand = "python3 transcription_client.py tests/resources/long-audio/long_test.mp3"
    os.system(syscommand)
    assert os.path.isfile(output_filepath + "/" + "s0j0.txt") and os.stat(output_filepath + "/" + "s0j0.txt").st_size > 5000