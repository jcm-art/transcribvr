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
    
    def execute_notebook_example(self):
        print("Loading Test Dataset")
        self.dataset = LibriSpeech("test-clean")
        self.loader = torch.utils.data.DataLoader(self.dataset, batch_size=16)

        print("Loading Model")
        self.model = whisper.load_model("base.en")
        print(
            f"Model is {'multilingual' if self.model.is_multilingual else 'English-only'} "
            f"and has {sum(np.prod(p.shape) for p in self.model.parameters()):,} parameters."
        )
        
        print("Configuring Model")
        # predict without timestamps for short-form transcription
        self.options = whisper.DecodingOptions(language="en", without_timestamps=True)

class LibriSpeech(torch.utils.data.Dataset):
    """
    A simple class to wrap LibriSpeech and trim/pad the audio to 30 seconds.
    It will drop the last few seconds of a very small portion of the utterances.
    """
    def __init__(self, split="test-clean", device=DEVICE):
        self.dataset = torchaudio.datasets.LIBRISPEECH(
            root=os.path.expanduser("~/.cache"),
            url=split,
            download=True,
        )
        self.device = device

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        audio, sample_rate, text, _, _, _ = self.dataset[item]
        assert sample_rate == 16000
        audio = whisper.pad_or_trim(audio.flatten()).to(self.device)
        mel = whisper.log_mel_spectrogram(audio)
        
        return (mel, text)


my_transcibvr = Transcibvr()
my_transcibvr.execute_notebook_example()