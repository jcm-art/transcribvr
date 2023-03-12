


audio_files = dict()
allowed_formats = ["mp3, m4a"]
INPUT_FILE_PATH = ".\\audio_input\\"


class AudioDataManager:
    
    def __init__(self):
        self.__log_entry("Initializing AudioDataManager")


    def process_audio_files(self, audio_file_path_list: list[str], job_id: str) -> dict: 
        return self.audio_files
    
    #def process_audio_files(audio_files: dict, job_id: str) -> dict: 
    #    return audio_files
    
    def get_audio_file_paths(self, job_id: str) -> dict:
        return self.audio_files[job_id]
    
    def clear_audio_buffer(self, job_id: str) -> bool:
        return False
    
    def __check_file_format(self, audio_filename: str) -> bool:
        self.__log_entry("Verifying file name exists")
        return False

    def __check_audio_format(self, audio_filename: str) -> bool:
        self.__log_entry("Verifying audio file format allowed")
        return False
    
    def __load_audio(self, audio_filename: str) -> bool:
        self.__log_entry("Loading audio file")
        return False
    
    def __convert_audio(self, audio_filename: str) -> bool:
        self.__log_entry("Converting audio file")
        return False
    
    def __save_audio_in_buffer(self, audio_filename: str) -> bool:
        self.__log_entry("Saving audio file")
        return False
    
    def __log_entry(self, entry: str):
        print(entry)