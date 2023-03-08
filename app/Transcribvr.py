import os
import numpy as np

import torch
import pandas as pd
import whisper
import torchaudio

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class Transcibvr:
    hello_text="Hello World"

    def __init__(self) -> None:
        pass

    def hello_world(self):
        print(self.hello_text) 

    def load_model(self):
        print("Loading Transciption Model")
        self.model = whisper.load_model("base.en")

my_transcibvr = Transcibvr()
my_transcibvr.hello_world()