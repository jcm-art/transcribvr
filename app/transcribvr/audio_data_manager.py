from pydub import AudioSegment
import os


class AudioDataManager:
    audio_files = {}
    allowed_formats = ("mp3, m4a")
    INPUT_FILEPATH = "./audio_input/"
    file_num=0

    def __init__(self):
        self.__log_entry("Initializing AudioDataManager")


    def process_audio_files(self, audio_file_paths: str, job_id: str) ->dict: 

        #Get current audio file path
        audio_file_path = audio_file_paths

        #Assign prefix for job and audio file
        buffer_audio_name = self.__assign_file_prefix(job_id)
    

        #Get audio file format
        audio_format = self.__get_audio_format(audio_file_path)

        #Check that audio format is in scope
        assert(self.__check_audio_format(audio_format))

        #TODO: handle file lists
        #TODO: handle zip files
        #TODO: assign_file_names
        audio_buffer_file = self.__load_audio(audio_file_path, buffer_audio_name, audio_format)

        self.audio_files[buffer_audio_name] = "METADATA PLACEHOLDER"

        return self.audio_files
    
    #def process_audio_files(audio_files: dict, job_id: str) -> dict: 
    #    return audio_files
    
    #TODO - test case for get audio file paths
    def get_audio_file_paths(self, job_id: str) -> list:
        file_path_list = []
        for file_ids in self.audio_files[job_id]:
            audio_buffer_file = file_ids + ".mp3"
            file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)
            file_path_list.append(file_path)
        return file_path_list
    
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
    
    def __get_audio_format(self, audio_filename: str) -> str:
        name_parts = audio_filename.split(".")
        audio_format = name_parts[-1]
        self.__log_entry("Audio format for %s is %s" % (audio_filename, audio_format))
        return audio_format

    def __check_audio_format(self, audio_format: str) -> bool:
        is_allowed = audio_format in self.allowed_formats
        self.__log_entry("Audio format is allowed = %s" % is_allowed)
        return is_allowed
    
    def __load_audio(self, audio_filename: str, buffer_audio_name: str, audio_format: str):
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
        audio_buffer_file = buffer_audio_name + ".mp3"
        file_path = os.path.join(self.INPUT_FILEPATH, audio_buffer_file)

        audio_object.export(file_path, format="mp3")

        self.__log_entry("Converting and saving " + audio_buffer_file)
        
        return audio_buffer_file
    
    def __log_entry(self, entry: str):
        print(entry)