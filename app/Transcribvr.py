import os
import numpy as np

import torch
import pandas as pd
import whisper
import torchaudio
from pydub import AudioSegment

if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyTorch install was not "
              "built with MPS enabled.")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ "
              "and/or you do not have an MPS-enabled device on this machine.")
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
else:
    DEVICE = torch.device("mps")

class Transcibvr:
    hello_text="Hello World"

    def __init__(self) -> None:
        pass

    def hello_world(self):
        print(self.hello_text) 

    def load_model(self):
        print("Loading Transciption Model")
        self.model = whisper.load_model("base.en")

    def convert_audio(sekf):
        # files                                                                         
        src = "transcript.mp3"
        dst = "test.wav"

        # convert wav to mp3                                                            
        m4a_audio = AudioSegment.from_file("audio.m4a", format="m4a")
        m4a_audio.export("audio.mp3", format="mp3")
    
    def load_audio(self):
        # load audio and pad/trim it to fit 30 seconds
        self.audio = whisper.load_audio("audio.mp3")
        self.audio = whisper.pad_or_trim(self.audio)
    
    def make_log_mel_spectrogram(self):
        # make log-Mel spectrogram and move to the same device as the model
        self.mel = whisper.log_mel_spectrogram(self.audio).to(self.model.device)
    
    def detect_language(self):
        # detect the spoken language
        _, probs = self.model.detect_language(self.mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

    def decode_audio(self):
        # decode the audio
        if DEVICE=="cpu":
                self.options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16 = False)
        else:
            self.options = whisper.DecodingOptions(language="en", without_timestamps=True)
 
        self.result = whisper.decode(self.model, self.mel, self.options)

    def output_audio(self):
        # print the recognized text
        print(self.result.text)

my_transcibvr = Transcibvr()
my_transcibvr.hello_world()
my_transcibvr.load_model()
my_transcibvr.convert_audio()
my_transcibvr.load_audio()
my_transcibvr.make_log_mel_spectrogram()
my_transcibvr.decode_audio()
my_transcibvr.output_audio()