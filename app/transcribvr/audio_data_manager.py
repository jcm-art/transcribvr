from pydub import AudioSegment
import os


class AudioDataManager:
    audio_files = {}
    allowed_formats = ["mp3, m4a"]
    INPUT_FILEPATH = "./audio_input/"
    file_num=0

    def __init__(self):
        self.__log_entry("Initializing AudioDataManager")


    def process_audio_files(self, audio_file_paths: str, job_id: str) ->dict: 
        #TODO: check file format
        #TODO: check audio format
        #TODO: handle file lists
        audio_file_path = audio_file_paths
        #TODO: handle zip files
        #TODO: assign_file_names
        buffer_audio_name = self.__assign_file_prefix(job_id)
        audio_object = self.__load_audio(audio_file_path)
        audio_buffer_file = self.__convert_audio_to_buffer(audio_object, buffer_audio_name)

        self.audio_files[buffer_audio_name] = "METADATA PLACEHOLDER"

        return self.audio_files
    
    #def process_audio_files(audio_files: dict, job_id: str) -> dict: 
    #    return audio_files
    
    def get_audio_file_paths(self, job_id: str) -> dict:
        return self.audio_files[job_id]
    
    def clear_audio_buffer(self, job_id: str) -> bool:
        return False
    
    def get_buffer_filepath(self) -> str:
        return self.INPUT_FILEPATH

    def __assign_file_prefix(self, job_id: str) -> str:
        current_filename = job_id + "f" + str(self.file_num)
        self.__log_entry("Assigning file name of " + current_filename)
        return current_filename

    def __check_file_format(self, audio_filename: str) -> bool:
        self.__log_entry("Verifying file name exists")
        return False

    def __check_audio_format(self, audio_filename: str) -> bool:
        self.__log_entry("Verifying audio file format allowed")
        return False
    
    def __load_audio(self, audio_filename: str):
        m4a_audio = AudioSegment.from_file(audio_filename, format="m4a")

        self.__log_entry("Loaded " + audio_filename)

        return m4a_audio
    
    def __convert_audio_to_buffer(self, audio_object, buffer_audio_name: str) -> str:
        audio_buffer_file = buffer_audio_name + ".mp3"
        file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)

        audio_object.export(file_path, format="mp3")

        self.__log_entry("Converting and saving " + audio_buffer_file)
        
        return audio_buffer_file
    
    def __log_entry(self, entry: str):
        print(entry)