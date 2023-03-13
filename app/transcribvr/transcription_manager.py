from transcribvr.audio_data_manager import AudioDataManager
from transcribvr.audio_transcriber import AudioTranscriber
from transcribvr.output_manager import OutputManager

class TranscriptionManager:
    INPUT_FILEPATH = "./audio_input/"
    job_id=0
    job_packages = {}

    def __init__(self):
        self.__log_entry("Initializing TranscriptionManager")
        self.session_id=self.__define_session_id()
        self.audioLoader = AudioDataManager()
        self.audioTranscriber = AudioTranscriber()
        self.outputManager = OutputManager()

        self.__log_entry("Session %s ready for transcription task" % self.session_id)


    def check_if_ready_for_transcription(self):
        if self.audioLoader and self.audioTranscriber and self.outputManager:
            return True
        else:
            return False

    def assign_transcription(self,audio_file_path: str) -> str:
        self.__log_entry("Assign transcription task")
        current_job_id = self.__generate_job_id()
        self.job_packages[current_job_id]= audio_file_path

        self.__log_entry("Prepare audio files for " + current_job_id)

        self.__log_entry("Dictionary (to data manager): \n " + str(self.job_packages[current_job_id]))

        self.job_packages[current_job_id] = self.__prepare_audio(self.job_packages[current_job_id], current_job_id)

        self.__log_entry("Dictionary (from data manager): \n " + str(self.job_packages))

        self.job_packages[current_job_id] = self.__transcribe_audio(self.job_packages[current_job_id],current_job_id)

        self.__log_entry("Dictionary (from transcriber): \n " + str(self.job_packages))

        output_text = self.__generate_output(current_job_id)

        self.__log_entry("Final Output Text: \n " + output_text + " finished.")

        return ""
    
    def get_buffer_filepath(self):
        return self.INPUT_FILEPATH

    def __prepare_audio(self, audio_files: str, job_id: str) -> dict:
        self.__log_entry("Prepare audio for job id %s " % job_id)
        processed_files = self.audioLoader.process_audio_files(audio_files, job_id)
        self.__log_entry("Processed files returned: \n" + str(processed_files))
        return processed_files
    
    def __transcribe_audio(self, transcription_package: dict, current_job_id: str) -> dict:
        transcription_output = self.audioTranscriber.transcribe_audio_in_buffer(transcription_package, current_job_id)
        self.__log_entry("Transcribed audio for job %s to output: " % current_job_id)
        self.__log_entry(str(transcription_output))
        
        return transcription_output
    
    def __generate_output(self, current_job_id) -> bool:
        self.__log_entry("Generate transcription output")
        output_text = self.outputManager.generate_ouput_text(self.job_packages[current_job_id], current_job_id)
        return output_text
    
    def __dispatch_output(self) -> bool:
        self.__log_entry("Dispatch transcription output")
        return False
    
    def __define_session_id(self) -> int:
        self.__log_entry("Generate session id")
        session_id = 0
        return session_id
    
    def __generate_job_id(self) -> str:
        current_job_id = "s" + str(self.session_id) + "j" + str(self.job_id)
        self.job_id+=1

        self.__log_entry("Generated job id: %s" % current_job_id)
        return current_job_id

    def __log_entry(self, entry: str):
        print(entry)