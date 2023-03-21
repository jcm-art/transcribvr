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
        
        # Get identifier 
        current_task_id_str = self.__get_job_id_str(self.session_num, job_num)

        # Start building job filestructure
        # TODO - Update dictionary in sub method to clean up
        self.job_packages[current_task_id_str]= audio_file_paths

        # Audio Data manager preprocessing of audio files
        # TODO - log in submethod
        self.__log_entry(f"Prepare audio files for {current_task_id_str}")
        self.__log_entry("Dictionary (to data manager): \n " + str(self.job_packages[current_task_id_str]))
        # Replace audio file list in dictionary with metadata and locations of files in buffer
        # TODO - Update dictionary in sub method to clean up
        self.job_packages[current_task_id_str] = self.__prepare_audio(
            self.job_packages[current_task_id_str], 
            current_task_id_str)
        # TODO - log in submethod
        self.__log_entry("Dictionary (from data manager): \n " + str(self.job_packages))

        # Transcription of audio files in buffer
        # TODO - Update dictionary in sub method to clean up
        self.job_packages[current_task_id_str] = self.__transcribe_audio(
            self.job_packages[current_task_id_str],
            current_task_id_str)
        # TODO - log in submethod
        self.__log_entry("Dictionary (from transcriber): \n " + str(self.job_packages))

        # Format output text from transcription distionary
        output_text = self.__generate_output(current_task_id_str)
        # TODO - log in submethod
        self.__log_entry("Final Output Text: \n " + output_text + " finished.")

        # Dispatch output
        # TODO - return file name for command line application

        return output_text

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

    def __prepare_audio(self, audio_file_list: list, task_id_str: str) -> dict:
        """
        Prepare the specified audio files for transcription.

        Args:
            audio_files (str): A string representing the path to the audio file(s) to be transcribed.
            job_id (str): A string representing the unique identifier for the current transcription job.

        Returns:
            dict: A dictionary containing the processed audio files, ready for transcription.

        """
        self.__log_entry("Prepare audio for job id %s " % task_id_str)
        processed_files = self.audioLoader.process_audio_files(audio_file_list, task_id_str)
        self.__log_entry("Processed files returned: \n" + str(processed_files))
        return processed_files
    
    def __transcribe_audio(self, transcription_package: dict, task_id_str: str) -> dict:
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
        transcription_output = self.audioTranscriber.transcribe_audio_in_buffer(transcription_package, task_id_str)
        self.__log_entry("Transcribed audio for job %s to output: " % task_id_str)
        self.__log_entry(str(transcription_output))
        
        return transcription_output
    
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