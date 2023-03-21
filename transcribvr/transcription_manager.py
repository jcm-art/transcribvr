from audio_data_manager import AudioDataManager
from audio_transcriber import AudioTranscriber
from output_manager import OutputManager

class TranscriptionManager:
    """
    A class that takes audio files or audio file paths from an external client, converts 
    the audio to MP3 format, generates a transcription of the audio via a transcription 
    class, formats the output via an output manager, and dispatches the output to the client.
    """
    
    # TODO - remove this?
    INPUT_FILEPATH = "./audio_input/"
    job_packages = {}
    # TODO - move metadata tags into static global constants

    def __init__(self, session_num):
        """
        Constructor for the TranscriptionManager class. Initializes object attributes and 
        sets up a new transcription session.

        Args:
        None.

        Returns:
        None.

        """
        self.__log_entry("Initializing TranscriptionManager")
        # Assign session number to TM
        self.session_num = session_num

        # Load other motdules needed for transcription
        self.audioLoader = AudioDataManager()
        self.audioTranscriber = AudioTranscriber()
        self.outputManager = OutputManager()

        #Log ready to start
        self.__log_entry("Session %s ready for transcription task" % self.session_num)

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

    # TODO - break into dispatch method to enable future multithreaded expansion
    # TODO - have transcription manager build dict structure
    def assign_transcription(self,audio_file_paths: list, job_num: int) -> str:
        """
        Assign a transcription task for the specified audio file.

        Args:
            audio_file_path (str): A string representing the path to the audio file to 
                be transcribed.

        Returns:
            str: output text of the transcription

        """
        self.__log_entry("Assign transcription task")
        # Get task ID string for assignment
        current_task_id_str = self.__get_job_id_str(self.session_num, job_num)

        # Initialize global dictionary with task ID string
        self.job_packages[current_task_id_str]= -1

        # Dispatch task - currently single threaded, potentially multithreaded in the future
        # Replace global package with output dictionary
        return self.__dispatch_task(audio_file_paths, current_task_id_str)
        

    # TODO - remove this?
    def get_buffer_filepath(self):
        """
        Get the path to the directory where audio buffer files are stored.

        Args:
            None.

        Returns:
            str: A string representing the path to the audio buffer file directory.

        """
        return self.INPUT_FILEPATH

    def __dispatch_task(self, audio_file_paths: list, current_task_id_str: str):
        '''
        '''
        # Define package for job
        current_package ={}

        # Start building job filestructure
        current_package["task_id"] = current_task_id_str
        current_package["queued_filepaths"] = audio_file_paths
        self.__log_entry(f"Package initiated for {current_task_id_str}: \n {current_package}")

        # Audio Data manager preprocessing of audio files
        # Add filepaths for conditioned audio files in audio_input to current_package
        adm_package = self.__prepare_audio(
            current_package["queued_filepaths"], 
            current_task_id_str)
        current_package["preprocessed_audio"] = adm_package
        self.__log_entry(f"Package post AudioDataManager for {current_task_id_str}: \n {current_package}")


        # Transcription of audio files in buffer
        tm_package = self.__transcribe_audio(
            current_package["preprocessed_audio"],
            current_task_id_str)
        current_package["transcription_output"] = tm_package
        self.__log_entry(f"Package post TranscriptioManager for {current_task_id_str}: \n {current_package}")

        # Format output text from transcription distionary
        transcription_output, ouput_file_location = self.__generate_output(current_package, current_task_id_str)

        # Current package to global package
        self.__add_package_to_global(current_package, current_task_id_str)

        # Dispatch output
        self.__dispatch_output(transcription_output, current_task_id_str)

        self.__log_entry("Finished with transcription task")

        return ouput_file_location

    def __prepare_audio(self, audio_file_list: list, task_id_str: str) -> dict:
        """
        Prepare the specified audio files for transcription.

        Args:
            audio_files (str): A string representing the path to the audio file(s) to be transcribed.
            job_id (str): A string representing the unique identifier for the current transcription job.

        Returns:
            dict: A dictionary containing the processed audio files, ready for transcription.

        """
        self.__log_entry(f"Prepare audio files for {task_id_str}")
        # Get audio input buffer files and initial metadata
        adm_package = self.audioLoader.process_audio_files(audio_file_list, task_id_str)
        return adm_package
    
    def __transcribe_audio(self, preprocessed_audio: dict, task_id_str: str) -> dict:
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
        self.__log_entry(f"Transcribe audio files for {task_id_str}")
        transcription_package = self.audioTranscriber.transcribe_audio_in_buffer(
            preprocessed_audio, task_id_str)
        return transcription_package
    
    def __generate_output(self, current_package: dict, task_id_str: str ) -> str:
        """
        Generate the transcription output text for the specified job.

        Args:
            current_job_id (str): A string representing the unique identifier for the current 
                transcription job.

        Returns:
            str: The transcription output text for the specified job.

        """
        self.__log_entry("Generate transcription output")
        output_text, output_file_location = self.outputManager.generate_ouput_text(current_package, task_id_str)
        return output_text, output_file_location
    
    def __add_package_to_global(self,current_package, task_id_str):
        self.job_packages[task_id_str]= current_package


    def __get_job_id_str(self, session_num, job_num) -> str:
        '''Method returns a string with the session number and job number for JSPON structure'''
        return f"s{session_num}j{job_num}"

    def __dispatch_output(self, transcription_output: str, current_task_id_str: str) -> bool:
        self.__log_entry("Dispatch transcription output")
        self.__log_entry(f"Final output text is: \n {transcription_output}")

    def __log_entry(self, entry: str):
        """
        Log the specified entry.

        Args:
            entry (str): A string representing the log entry to be recorded.

        """
        print("TranscriptionManager: " + entry)