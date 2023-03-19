import os
import numpy as np
import time

import torch
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

    def save_all_data(self):
        file_prefix = "libri-test-clean/libri-test-clean-sample"
        import_format = ".wav"
        export_formats = ("mp3", "m4a","acc","ogg","flac","aiff")
        # Missing: "alac", "dsd", "pcm"

        for index in range(0,1):
            (audio_waveform, sample_rate, transcript) = self.__getitem__(index)

            audio_path = file_prefix + ("%s" % index)
            transcript_path = file_prefix + ("%s" % index) + ".txt"

            torchaudio.save(audio_path+import_format, audio_waveform, sample_rate)

            if index <1:
                self.__save_alternate_formats(audio_path, export_formats)

            with open(transcript_path, 'w') as f:
                f.write(transcript)


    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        audio_waveform, sample_rate, text, soeaker_id, chapter_id, utterance_id = self.dataset[item]
        assert sample_rate == 16000
        
        return (audio_waveform, sample_rate, text)
    
    def __save_alternate_formats(self, path, export_formats):
        audio_waveform = AudioSegment.from_wav(path+".wav")

        for format in export_formats:
            if format == "m4a":
                self.__save_in_format(audio_waveform, path, "."+format, "ipod")
            elif format =="acc":
                self.__save_in_format(audio_waveform, path, "."+format, "adts")
            else:
                self.__save_in_format(audio_waveform, path,  "."+format, format)

    def __save_in_format(self, audio_waveform, path, file_extention, format):
        audio_waveform.export(path + file_extention, format=format)


class LibriSpeechTestData:
    
    def __init__(self) -> None:
        pass

    def execute_dataset_procurement(self):
        self.load_test_dataset("test-clean")
        self.save_dataset()

    def load_test_dataset(self, dataset_name):
        print("Loading Test Dataset")
        self.dataset = LibriSpeech(dataset_name)

    def save_dataset(self):
         print("Saving test dataset")
         self.dataset.save_all_data()
        
    def clear_dataset(self):
         print("Clearing test dataset")
         folder_path = "libri-test-clean"
         files_to_delete = os.listdir(folder_path)
         for file in files_to_delete:
             os.remove(folder_path + "/" + file)

my_librianalyzer = LibriSpeechTestData()

my_librianalyzer.execute_dataset_procurement()
time.sleep(2)
my_librianalyzer.clear_dataset()