


OUTPUT_FILEPATH =".\\transcription_output\\"

class OutputManager:
    
    def __init__(self):
        self.__log_entry("Initializing OutputManager")

    def generate_ouput_text(self,transcription_dict: dict) -> str:
        self.__log_entry("Generating output text")
        return ""
    
    def set_custom_filepath(self,custom_output_filepath) -> bool:
        self.__log_entry("Updating file path")
        return False
    
    def __log_entry(self, entry: str):
        print(entry)