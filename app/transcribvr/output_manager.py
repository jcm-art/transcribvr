import os


class OutputManager:
    OUTPUT_FILEPATH ="./transcription_output/"

    def __init__(self):
        self.__log_entry("Initializing OutputManager")

    def generate_ouput_text(self,transcription_dict: dict, current_job_id: str) -> str:
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
        self.__log_entry("Updating file path")
        return False
    
    def __save_output_file(self, output_text: str, current_job_id: str)-> bool:
        name_of_file = current_job_id + ".txt"
        output_filename = os.path.join(self.OUTPUT_FILEPATH, name_of_file)         
        output_file = open(output_filename, "w")
        output_file.write(output_text)
        output_file.close()
        return True

    def __log_entry(self, entry: str):
        print(entry)