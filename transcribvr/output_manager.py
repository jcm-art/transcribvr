import os


class OutputManager:
    """
    A class to manage formatting the output of transcription tasks

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

    def generate_ouput_text(self, job_package: dict, current_job_id: str) -> str:
        """
        Generates the output text for a given transcription dictionary and job ID.

        Args:
            transcription_dict (dict): A dictionary containing the transcribed data.
            current_job_id (str): An identifier for the current job.

        Returns:
            str: The output text generated from the transcription dictionary.

        """
        self.__log_entry(f"Generating output for {current_job_id}\n {job_package}")

        output_text=f"Transcript for transcribvr task {current_job_id}.\n"
        
        preprocessed_dictionary = job_package['preprocessed_audio']
        transcript_dictionary = job_package['transcription_output']
        #self.__log_entry(preprocessed_dictionary)
        #self.__log_entry(transcript_dictionary)


        for item in transcript_dictionary.keys():
            # Retreived preprocessed metadata
            preprocessed_item = preprocessed_dictionary[item]
            transcript_item = transcript_dictionary[item]

            # Unpack metadata
            duration = preprocessed_item['duration_seconds']
            language = transcript_item['language']
            transcript = transcript_item['transcription']
            
            output_text+=f"\t Transcription for file {item} \n"
            output_text+=f"\t\t Duration: {duration} \n"
            output_text+=f"\t\t Language: {language} \n"
            output_text+=f"\t\t Transcript: {transcript} \n"

        ouput_file_location = self.__save_output_file(output_text, current_job_id)
        return output_text, ouput_file_location
    
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
        return output_filename

    def __log_entry(self, entry: str):
        """
        Logs an entry to track the progress of the output generation.

        Args:
            entry (str): The log entry to be saved.

        Returns:
            None.
        """
        print(entry)