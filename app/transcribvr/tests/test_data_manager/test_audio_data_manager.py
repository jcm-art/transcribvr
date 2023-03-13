from transcribvr.audio_data_manager import AudioDataManager

def test_buffer_filepath():
    adm = AudioDataManager()
    assert adm.get_buffer_filepath()=="./audio_input/"
