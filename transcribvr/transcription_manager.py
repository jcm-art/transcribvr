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
        self.job_packages[current_task_id_str]= self.__dispatch_task(audio_file_paths, current_task_id_str)
        

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
        self.__log_entry(f"""Package initiated for {current_task_id_str}: \n
                            {current_package[current_task_id_str]}""")

        # Audio Data manager preprocessing of audio files
        # Add filepaths for conditioned audio files in audio_input to current_package
        audio_input_files, adm_metadata = self.__prepare_audio(
            current_package["queued_filepaths"], 
            current_task_id_str)
        current_package["audio_input_filepaths"] = audio_input_files
        current_package["audio_data_manager_metadata"] = adm_metadata
        self.__log_entry(f"""Package post AudioDataManager for {current_task_id_str}: \n 
                            {current_package[current_task_id_str]}""")


        # Transcription of audio files in buffer
        transcript, tm_metadata = self.__transcribe_audio(
            current_package["audio_input_filepaths"],
            current_task_id_str)
        current_package["audio_transcript"] = transcript
        current_package["transcription_metadata"] = tm_metadata
        self.__log_entry(f"""Package post AudioDataManager for {current_task_id_str}: \n 
                            {current_package[current_task_id_str]}""")

        # Format output text from transcription distionary
        output_text = self.__generate_output(current_task_id_str)
        # TODO - log in submethod
        self.__log_entry("Final Output Text: \n " + output_text + " finished.")

        # Dispatch output
        # TODO - return file name for command line application

        return output_text

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
        processed_files, adm_metadata = self.audioLoader.process_audio_files(audio_file_list, task_id_str)
        return processed_files, adm_metadata
    
    def __transcribe_audio(self, audio_input_file_list: list, duration_list: list, task_id_str: str) -> dict:
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
        transcription_output, tm_metadata = self.audioTranscriber.transcribe_audio_in_buffer(
            audio_input_file_list,duration_list, task_id_str)
        
        return transcription_output, tm_metadata
    
    def __generate_output(self, task_id_str) -> str:
        """
        Generate the transcription output text for the specified job.

        Args:
            current_job_id (str): A string representing the unique identifier for the current 
                transcription job.

        Returns:
            str: The transcription output text for the specified job.

        """
        self.__log_entry("Generate transcription output")
        output_text = self.outputManager.generate_ouput_text(self.job_packages[task_id_str], task_id_str)
        return output_text
    
    def __get_job_id_str(self, session_num, job_num) -> str:
        '''Method returns a string with the session number and job number for JSPON structure'''
        return f"s{session_num}j{job_num}"

    def __dispatch_output(self, task_id_str) -> bool:
        self.__log_entry("Dispatch transcription output")
        #TODO - implement output dispatch
        return False

    def __log_entry(self, entry: str):
        """
        Log the specified entry.

        Args:
            entry (str): A string representing the log entry to be recorded.

        """
        print("TranscriptionManager: " + entry)