import os


class OutputManager:
    """
    Attributes:
        OUTPUT_FILEPATH (str): The default path where the output files are saved.

    Methods:
        __init__():
            Initializes the OutputManager object.

        generate_output_text(transcription_dict: dict, current_job_id: str) -> str:
            Generates the output text for a given transcription dictionary and job ID.

        set_custom_filepath(custom_output_filepath) -> bool:
            Sets a custom file path for the output file.

        __save_output_file(output_text: str, current_job_id: str)-> bool:
            Saves the output file with the given output text and job ID.

        __log_entry(entry: str):
            Logs an entry to track the progress of the output generation.

    """
    OUTPUT_FILEPATH ="./transcription_output/"

    def __init__(self):
        """
        Initializes the OutputManager object.

        Args:
            None.

        Returns:
            None.

        """
        self.__log_entry("Initializing OutputManager")

    def generate_ouput_text(self,transcription_dict: dict, current_job_id: str) -> str:
        """
        Generates the output text for a given transcription dictionary and job ID.

        Args:
            transcription_dict (dict): A dictionary containing the transcribed data.
            current_job_id (str): An identifier for the current job.

        Returns:
            str: The output text generated from the transcription dictionary.

        """
        self.__log_entry("Generating output text")

        output_text=""
        for transcript in transcription_dict:
            self.__log_entry("Generating output for " + str(transcript))
            self.__log_entry("Generating output for " + str(transcription_dict[transcript]))
            output_text+="Transcription for file " + transcript + "\n\n"
            output_text+="Metadata: " + str(transcription_dict[transcript]["metadata"])+ "\n\n"
            output_text+="Transcript: " + str(transcription_dict[transcript]["transcription"])+ "\n"

        assert(self.__save_output_file(output_text, current_job_id))
        return output_text
    
    def set_custom_filepath(self,custom_output_filepath) -> bool:
        """
        Sets a custom file path for the output file.

        Args:
            custom_output_filepath (str): The custom output file path.

        Returns:
            bool: True if the custom file path was set successfully.

        """
        self.__log_entry("Updating file path")
        return False
    
    def __save_output_file(self, output_text: str, current_job_id: str)-> bool:
        """
        Saves the output file with the given output text and job ID.

        Args:
            output_text (str): The output text to be saved.
            current_job_id (str): An identifier for the current job.

        Returns:
            bool: True if the output file was saved successfully.
        """
        name_of_file = current_job_id + ".txt"
        output_filename = os.path.join(self.OUTPUT_FILEPATH, name_of_file)         
        output_file = open(output_filename, "w")
        output_file.write(output_text)
        output_file.close()
        return True

    def __log_entry(self, entry: str):
        """
        Logs an entry to track the progress of the output generation.

        Args:
            entry (str): The log entry to be saved.

        Returns:
            None.
        """
        print(entry)