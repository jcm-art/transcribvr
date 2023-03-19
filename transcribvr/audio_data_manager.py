from pydub import AudioSegment
import os


class AudioDataManager:
    """
    A class for managing audio files.

    Attributes:
    audio_files (dict): A dictionary to store audio file names and their metadata.
    allowed_formats (tuple): A tuple of allowed audio file formats.
    INPUT_FILEPATH (str): A string containing the path to the input directory.
    file_num (int): An integer to keep track of the number of audio files.

    Methods:
    __init__(self): Initializes AudioDataManager object.
    process_audio_files(self, audio_file_paths: str, job_id: str) -> dict: Processes the given audio files and returns a dictionary containing file names and metadata.
    get_audio_file_paths(self, job_id: str) -> list: Returns a list of file paths for the audio files belonging to the given job ID.
    clear_audio_buffer(self, job_id: str) -> bool: Clears the audio buffer for the given job ID.
    get_buffer_filepath(self) -> str: Returns the input directory path.
    __assign_file_prefix(self, job_id: str) -> str: Assigns a prefix to the audio file name based on the job ID and the file number.
    __check_file_format(self, audio_filename: str) -> bool: Verifies whether the audio file format is allowed.
    __get_audio_format(self, audio_filename: str) -> str: Extracts the audio file format from the file name.
    __check_audio_format(self, audio_format: str) -> bool: Verifies whether the audio file format is allowed.
    __load_audio(self, audio_filename: str, buffer_audio_name: str, audio_format: str): Loads the audio file into the audio buffer.
    __convert_audio_to_buffer(self, audio_object, buffer_audio_name: str) -> str: Converts the audio file to mp3 format and saves it in the input directory.
    __log_entry(self, entry: str): Prints the given string to the console.
    """

    audio_files = {}
    allowed_formats = ("mp3", "m4a")
    INPUT_FILEPATH = "./audio_input/"
    file_num=0


    def __init__(self):
        """
        Initializes the AudioDataManager object.
        """

        self.__log_entry("Initializing AudioDataManager")


    def process_audio_files(self, audio_file_paths: str, job_id: str) ->dict: 
        """
        Processes the given audio files and returns a dictionary containing file names and metadata.

        Args:
        audio_file_paths (str): A string containing the path of the audio file.
        job_id (str): A string containing the job ID.

        Returns:
        dict: A dictionary containing file names and metadata.
        """

        #TODO: handle file lists
        #TODO: handle zip files
        #TODO: assign_file_names
        #Get current audio file path
        audio_file_path = audio_file_paths

        #Assign prefix for job and audio file
        buffer_audio_name = self.__assign_file_prefix(job_id)
    

        #Get audio file format
        audio_format = self.__get_audio_format(audio_file_path)

        #Check that audio format is in scope
        if self.__check_audio_format(audio_format):
            audio_buffer_file = self.__load_audio(audio_file_path, buffer_audio_name, audio_format)
            self.audio_files[buffer_audio_name] = "METADATA PLACEHOLDER"

        return self.audio_files
    
    #def process_audio_files(audio_files: dict, job_id: str) -> dict: 
    #    return audio_files
    
    #TODO - test case for get audio file paths
    def get_audio_file_paths(self, job_id: str) -> list:
        """
        Returns a list of file paths for the audio files belonging to the given job ID.

        Args:
        job_id (str): A string containing the job ID.

        Returns:
        list: A list containing the filepaths for a job
        """

        file_path_list = []
        for file_ids in self.audio_files[job_id]:
            audio_buffer_file = file_ids + ".mp3"
            file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)
            file_path_list.append(file_path)
        return file_path_list
    
    def clear_audio_buffer(self, job_id: str) -> bool:
        """
        TODO: Implement function

        Clears the audio buffer for the given job_id.

        :param job_id: The ID of the job.
        :type job_id: str

        :return: True if the audio buffer was cleared successfully, False otherwise.
        :rtype: bool
        """
        return False
    
    def get_buffer_filepath(self) -> str:
        """
        Returns the filepath of the audio input folder.

        :return: The filepath of the audio input folder.
        :rtype: str
        """
        return self.INPUT_FILEPATH

    def __assign_file_prefix(self, job_id: str) -> str:
        """
        Assigns a file prefix for the given job_id.

        :param job_id: The ID of the job.
        :type job_id: str

        :return: The file prefix for the given job_id.
        :rtype: str
        """
        current_filename = job_id + "f" + str(self.file_num)
        self.__log_entry("Assigning file name of " + current_filename)
        return current_filename

    def __check_file_format(self, audio_filename: str) -> bool:
        """
        TODO: Implement function

        Checks if the given audio file format is acceptable for the AudioDataManager

        :param audio_filename: The name of the audio file.
        :type audio_filename: str

        :return: True if the audio format is compatible, False otherwise.
        :rtype: bool
        """
        self.__log_entry("Verifying file name exists")
        return False
    
    def __get_audio_format(self, audio_filename: str) -> str:
        """
        Given an audio filename as a string, return the audio format as a string. The audio 
        format is defined as the file extension of the input filename.

        Args:
            audio_filename (str): A string representing the filename of the audio file.

        Returns:
            str: A string representing the audio format of the input file.

        Raises:
            None.

        Example:
            If audio_filename is "song.mp3", this method returns "mp3".
        """
        name_parts = audio_filename.split(".")
        audio_format = name_parts[-1]
        self.__log_entry("Audio format for %s is %s" % (audio_filename, audio_format))
        return audio_format

    def __check_audio_format(self, audio_format: str) -> bool:
        """
        Given an audio format as a string, determine if it is allowed based on the 
        'allowed_formats' attribute of this object.

        Args:
            audio_format (str): A string representing the audio format to be checked.

        Returns:
            bool: True if the input audio format is allowed and False otherwise.

        Raises:
            None.
        """

        is_allowed = audio_format in self.allowed_formats
        self.__log_entry("Audio format is allowed = %s" % is_allowed)
        return is_allowed
    
    def __load_audio(self, audio_filename: str, buffer_audio_name: str, audio_format: str):
        """
        Given an audio filename as a string, load the corresponding audio file into memory 
        and return the path to the loaded file. The loaded file is stored in a temporary 
        buffer file with the name specified by 'buffer_audio_name'.

        Args:
            audio_filename (str): A string representing the filename of the audio file 
                to be loaded.
            buffer_audio_name (str): A string representing the base name of the temporary 
                buffer file used to store the loaded audio data.
            audio_format (str): A string representing the format of the input audio file.

        Returns:
            str: A string representing the path to the temporary buffer file containing 
                the loaded audio data.

        Raises:
            None.
        """

        audio_buffer_file = ""
        if audio_format == "mp3":
            os.system('cp %s %s' % (audio_filename,buffer_audio_name))  
            audio_buffer_file = buffer_audio_name+".mp3"
        else:
            m4a_audio = AudioSegment.from_file(audio_filename, format=audio_format)
            audio_buffer_file = self.__convert_audio_to_buffer(m4a_audio, buffer_audio_name)

        self.__log_entry("Loaded " + audio_filename)

        return audio_buffer_file
    
    def __convert_audio_to_buffer(self, audio_object, buffer_audio_name: str) -> str:
        """
        Given an audio object and a base name for a temporary buffer file, convert the 
        audio object to an MP3 file and save it to disk. Return the path to the saved file.

        Args:
            audio_object (AudioSegment): An object representing the loaded audio data.
            buffer_audio_name (str): A string representing the base name of the temporary 
                buffer file used to store the converted audio data.

        Returns:
            str: A string representing the path to the temporary buffer file containing 
                the converted audio data.

        Raises:
            None.
        """
        audio_buffer_file = buffer_audio_name + ".mp3"
        file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)

        audio_object.export(file_path, format="mp3")

        self.__log_entry("Converting and saving " + audio_buffer_file)
        
        return audio_buffer_file
    
    def __log_entry(self, entry: str):
        """
        Given a string representing a log entry, print the log entry to the console.

        Args:
            entry (str): A string representing the log entry to be printed.

        Returns:
            None.

        Raises:
            None.
        """
        print(entry)