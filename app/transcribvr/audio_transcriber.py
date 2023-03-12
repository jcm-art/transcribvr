

DEVICE = ""
#- model: [?]
#- options: [?]
audio_dict = dict()
transcription_dict = dict()

class AudioTranscriber:

    def __init__(self, high_perf=False):
        self.high_perf = high_perf
        self.__log_entry("Initializing %s AudioTranscriber" % 
                         ("high performance" if self.high_perf else "standard performance"))


    def transcribe_audio_in_buffer(audio_buffer: dict) -> dict:
        return transcription_dict

    def __parse_audio_dict(self, audio_filename: str) -> bool:
        self.__log_entry("Parsing audio dictionary")
        return False
    
    def __load_model(self) -> bool:
        self.__log_entry("Loading %s model" % ("high performance" if self.high_perf else "standard performance"))
        return False
    
    def __make_log_mel_spectrogram(self) -> bool:
        self.__log_entry("Making spectrogram for audio file")
        return False
    
    def __detect_language(self) -> bool:
        self.__log_entry("Making spectrogram for audio file")
        return False
    
    def __decode_audio(self) -> bool:
        self.__log_entry("Decoding audio file")
        return False

    def __log_entry(self, entry: str):
        print(entry)
