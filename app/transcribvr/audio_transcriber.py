import numpy as np
import os
import torch
import whisper
import torchaudio

class AudioTranscriber:
    DEVICE = ""
    INPUT_FILEPATH = "./audio_input/"
    LANGUAGE_DEFAULT = "N/A for standard performance model"
    transcription_dict = {}

    def __init__(self, high_perf=False):
        self.high_perf = high_perf
        self.__log_entry("Initializing %s AudioTranscriber" % 
                         ("high performance" if self.high_perf else "standard performance"))
        
        self.__define_device()
        self.__log_entry("Device in use is " + self.DEVICE)

        assert(self.__load_model())

    def transcribe_audio_in_buffer(self, audio_buffer: dict, job_id: str) -> dict:
        assert(self.__parse_audio_dict(audio_buffer, job_id))

        return self.transcription_dict[job_id]

    def __parse_audio_dict(self, audio_buffer: dict, job_id: str) -> bool:
        audio_entry={}
        self.__log_entry("Parsing audio dictionary")
        language = self.LANGUAGE_DEFAULT
    
        for audio_file in audio_buffer:
            metadata = audio_buffer[audio_file]
            self.__log_entry("Processing key %s with metadata %s" % (audio_file, metadata))

            audio = self.__load_audio(audio_file)
            mel_audio = self.__make_log_mel_spectrogram(audio)
            #TODO: add language support for higher perf models
            #language = self.__detect_language(mel_audio)
            result = self.__decode_audio(mel_audio)
            output_text = self.__get_ouput_text(result)


            audio_entry[audio_file] = {"metadata": 
                                            {"original metadata": metadata, 
                                             "language": language },
                                       "transcription": output_text}
            self.transcription_dict[job_id] = audio_entry
       
        return True
    
    def __define_device(self):
        if not torch.backends.mps.is_available():
            if not torch.backends.mps.is_built():
                print("MPS not available because the current PyTorch install was not "
                    "built with MPS enabled.")
            else:
                print("MPS not available because the current MacOS version is not 12.3+ "
                    "and/or you do not have an MPS-enabled device on this machine.")
            self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.DEVICE = torch.device("mps")
    
    def __load_model(self) -> bool:
        self.__log_entry("Loading %s model" % ("high performance" if self.high_perf else "standard performance"))
        self.model = whisper.load_model("base.en")
        return True
    
    def __load_audio(self, audio_file: str):
        audio_buffer_file = audio_file + ".mp3"
        file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)

        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)

        return audio
    
    def __make_log_mel_spectrogram(self, audio):
        self.__log_entry("Making spectrogram for audio file")
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        return mel
    
    def __detect_language(self, mel_audio) -> str:
        self.__log_entry("Detecting Language for audio file")
        _, probs = self.model.detect_language(mel_audio)
        language_detection = f"Detected language: {max(probs, key=probs.get)}"
        self.__log_entry(language_detection)
        return language_detection
    
    def __decode_audio(self, mel_audio):
        self.__log_entry("Decoding audio file")
        # decode the audio
        if self.DEVICE=="cpu":
                self.options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16 = False)
        else:
            self.options = whisper.DecodingOptions(language="en", without_timestamps=True)
 
        result = whisper.decode(self.model, mel_audio, self.options)

        return result
    
    def __get_ouput_text(self, result) -> str:
        output_text = result.text
        self.__log_entry("Output text is " + output_text)
        return output_text

    def __log_entry(self, entry: str):
        print(entry)
