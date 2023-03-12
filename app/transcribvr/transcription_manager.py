

INPUT_FILEPATH: str=".\\audio_input\\"
job_id=0

class TranscriptionManager:
    
    def __init__(self):
        self.__log_entry("Initializing TranscriptionManager")
        #self.audioLoader = AudioLoader()
        #self.audioTranscriber = AudioTranscriber()

    def assign_transcription(self,audio_file_path: str) -> bool:
        self.__log_entry("Assign transcription task")
        return False

    def __generate_job_id(self) -> bool:
        self.__log_entry("Generate job id")
        return False

    def __prepare_audio(self) -> bool:
        self.__log_entry("Prepare audio for job")
        return False
    
    def __transcribe_audio(self) -> bool:
        self.__log_entry("Transcribe audio for job")
        return False
    
    def __generate_output(self) -> bool:
        self.__log_entry("Generate transcription output")
        return False
    
    def __dispatch_output(self) -> bool:
        self.__log_entry("Dispatch transcription output")
        return False

    def __define_session_id(self) -> bool:
        self.__log_entry("Define session ID")
        return False

    def __log_entry(self, entry: str):
        print(entry)