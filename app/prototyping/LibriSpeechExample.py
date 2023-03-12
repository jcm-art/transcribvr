import os
import numpy as np

import torch
import pandas as pd
import whisper
import torchaudio
from tqdm import tqdm
import jiwer
from whisper.normalizers import EnglishTextNormalizer

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

class LibriSpeechAnalyzer:
    
    def __init__(self) -> None:
        pass

    def execute_notebook_example(self):
            self.load_test_dataset("test-clean")
            self.load_model("tiny.en")
            self.configure_model()
            self.model_decode_with_progress(2)
            #self.model_decode(2)
            self.show_data()
            self.show_word_error_rate()

    def load_test_dataset(self, dataset_name):
            print("Loading Test Dataset")
            self.dataset = LibriSpeech(dataset_name)
            self.loader = torch.utils.data.DataLoader(self.dataset, batch_size=16)
    
    def load_model(self, model_name):
            print("Loading Model")
            self.model = whisper.load_model(model_name)
            print(
                f"Model is {'multilingual' if self.model.is_multilingual else 'English-only'} "
                f"and has {sum(np.prod(p.shape) for p in self.model.parameters()):,} parameters."
            )
            
    def configure_model(self):
            print("Configuring Model")
            # predict without timestamps for short-form transcription
            if DEVICE=="cpu":
                self.options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16 = False)
            else:
                self.options = whisper.DecodingOptions(language="en", without_timestamps=True)
 
    def model_decode_with_progress(self,max_iterations):
            self.hypotheses = []
            self.references = []

            print("Decoding model with progress bar")

            counter = 0

            for mels, texts in tqdm(self.loader):
                if counter < max_iterations:
                    self.results = self.model.decode(mels, self.options)
                    self.hypotheses.extend([result.text for result in self.results])
                    self.references.extend(texts)
                    counter+=1
                else:
                    continue

    def model_decode(self,max_iterations):
        self.hypotheses = []
        self.references = []

        print("Decoding model without progress bar")

        counter = 0

        dataiter = iter(self.loader)

        for i in range(0,max_iterations):
            mels, texts = next(dataiter)
            self.results = self.model.decode(mels, self.options)
            self.hypotheses.extend([result.text for result in self.results])
            self.references.extend(texts)
    
    def show_data(self):
        self.data = pd.DataFrame(dict(hypothesis=self.hypotheses, reference=self.references))
        print(self.data)

    def show_word_error_rate(self):
        normalizer = EnglishTextNormalizer()
        self.data["hypothesis_clean"] = [normalizer(text) for text in self.data["hypothesis"]]
        self.data["reference_clean"] = [normalizer(text) for text in self.data["reference"]]
        print(self.data)

        wer = jiwer.wer(list(self.data["reference_clean"]), list(self.data["hypothesis_clean"]))

        print(f"WER: {wer * 100:.2f} %")

my_librianalyzer = LibriSpeechAnalyzer()

my_librianalyzer.execute_notebook_example()