from transcribvr.audio_data_manager import AudioDataManager
from transcribvr.audio_transcriber import AudioTranscriber
from transcribvr.output_manager import OutputManager

class TranscriptionManager:
    """
    A class that takes audio files or audio file paths from an external client, converts 
    the audio to MP3 format, generates a transcription of the audio via a transcription 
    class, formats the output via an output manager, and dispatches the output to the client.
    """
    
    INPUT_FILEPATH = "./audio_input/"
    job_id=0
    job_packages = {}

    def __init__(self):
        """
        Constructor for the TranscriptionManager class. Initializes object attributes and 
        sets up a new transcription session.

        Args:
        None.

        Returns:
        None.

        """
        self.__log_entry("Initializing TranscriptionManager")
        self.session_id=self.__define_session_id()
        self.audioLoader = AudioDataManager()
        self.audioTranscriber = AudioTranscriber()
        self.outputManager = OutputManager()

        self.__log_entry("Session %s ready for transcription task" % self.session_id)

    def check_if_ready_for_transcription(self):
        """
        Check if all necessary components for audio transcription are initialized and 
        ready to use.

        Args:
            None.

        Returns:
            bool: True if all necessary components are initialized, False otherwise.

        """
        if self.audioLoader and self.audioTranscriber and self.outputManager:
            return True
        else:
            return False

    def assign_transcription(self,audio_file_path: str) -> str:
        """
        Assign a transcription task for the specified audio file.

        Args:
            audio_file_path (str): A string representing the path to the audio file to 
                be transcribed.

        Returns:
            str: output text of the transcription

        """
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

        return output_text

    def get_buffer_filepath(self):
        """
        Get the path to the directory where audio buffer files are stored.

        Args:
            None.

        Returns:
            str: A string representing the path to the audio buffer file directory.

        """
        return self.INPUT_FILEPATH

    def __prepare_audio(self, audio_files: str, job_id: str) -> dict:
        """
        Prepare the specified audio files for transcription.

        Args:
            audio_files (str): A string representing the path to the audio file(s) to be transcribed.
            job_id (str): A string representing the unique identifier for the current transcription job.

        Returns:
            dict: A dictionary containing the processed audio files, ready for transcription.

        """
        self.__log_entry("Prepare audio for job id %s " % job_id)
        processed_files = self.audioLoader.process_audio_files(audio_files, job_id)
        self.__log_entry("Processed files returned: \n" + str(processed_files))
        return processed_files
    
    def __transcribe_audio(self, transcription_package: dict, current_job_id: str) -> dict:
        """
        Transcribe the audio contained within the specified transcription package.

        Args:
            transcription_package (dict): A dictionary containing the processed audio files ready for 
                transcription.
            current_job_id (str): A string representing the unique identifier for the current 
                transcription job.

        Returns:
            dict: A dictionary containing the transcribed text output for the current transcription job.

        """
        transcription_output = self.audioTranscriber.transcribe_audio_in_buffer(transcription_package, current_job_id)
        self.__log_entry("Transcribed audio for job %s to output: " % current_job_id)
        self.__log_entry(str(transcription_output))
        
        return transcription_output
    
    def __generate_output(self, current_job_id) -> str:
        """
        Generate the transcription output text for the specified job.

        Args:
            current_job_id (str): A string representing the unique identifier for the current 
                transcription job.

        Returns:
            str: The transcription output text for the specified job.

        """
        self.__log_entry("Generate transcription output")
        output_text = self.outputManager.generate_ouput_text(self.job_packages[current_job_id], current_job_id)
        return output_text
    
    def __dispatch_output(self) -> bool:
        self.__log_entry("Dispatch transcription output")
        return False
    
    def __define_session_id(self) -> int:
        """
        Define and return a unique identifier for the current session.

        Returns:
            int: An integer representing the unique identifier for the current session.

        """
        self.__log_entry("Generate session id")
        session_id = 0
        return session_id
    
    def __generate_job_id(self) -> str:
        """
        Generate and return a unique identifier for the current transcription job.

        Returns:
            str: A string representing the unique identifier for the current transcription job.

        """
        current_job_id = "s" + str(self.session_id) + "j" + str(self.job_id)
        self.job_id+=1

        self.__log_entry("Generated job id: %s" % current_job_id)
        return current_job_id

    def __log_entry(self, entry: str):
        """
        Log the specified entry.

        Args:
            entry (str): A string representing the log entry to be recorded.

        """
        print(entry)