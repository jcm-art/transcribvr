import os
import zipfile
from transcription_manager import TranscriptionManager

class TranscribvrServer:
    """
    A class that receives audio files from the Transcribvr Client classes for transcription processing
    """


    def __init__(self):
            """
            Constructor for the TranscribvrServer class. 

            Args:
            None.

            Returns:
            None.

            """
            self.__log_entry("Initializing TranscribvrServer")
            
            # Get absolute path to queued audio buffer to send files to
            self.__get_queued_buffer_filepath()

            # Define session and job ID
            self.session_id=self.__generate_session_id()
            self.job_id = 0

            # Instantiate transcription manager for use in jobs
            self.tm = TranscriptionManager(self.session_id)

    def assign_transcription_request(self, request_list):
        # Acknowledge receipt and print list of times to transcribe
        self.__log_entry("Receiving transcription request")
        for item in request_list:
            self.__log_entry(item)

        # Move audiofiles to buffer
        queued_request = self.__save_audio_to_queue(request_list)

        # Assign transcription task to transcription managaer
        if self.tm.check_if_ready_for_transcription():
            self.tm.assign_transcription(queued_request, self.job_id)
        else:
            self.__log_entry("Transcription manager is not ready, try again")

    def __get_queued_buffer_filepath(self):
        self.queued_audio_prefix = os.path.abspath("queued_audio") + "/"
        self.zip_audio_prefix = os.path.abspath("queued_audio/zip_audio") + "/"
        self.__log_entry("Location of audio file queue is " + self.queued_audio_prefix)


    def __save_audio_to_queue(self, request_list):
        queued_request = []
        counter = 0
        i=0
        while i < len(request_list):
            audio_file_path=request_list[i]
            _, post_fix = audio_file_path.split(".")

            if post_fix=="zip":
                request_list.extend(self.__handle_zip_files(audio_file_path))
            else:
                #TODO - move session and job management to this class
                queued_file_path = self.queued_audio_prefix + str(counter) + "." + post_fix
                os.system('cp %s %s' % (audio_file_path, queued_file_path)) 
                self.__log_entry(f"Location of new filepath is {queued_file_path}")
                queued_request.append(queued_file_path)
                counter+=1
            i+=1
        
        return queued_request

    def __handle_zip_files(self,file_path):
        zip_list = []
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(self.zip_audio_prefix)
            transcription_files = os.listdir(self.zip_audio_prefix)
            for file in transcription_files:
                zip_list.append(self.zip_audio_prefix + file)
        return zip_list

    def __generate_session_id(self) -> int:
        """
        Define and return a unique identifier for the current session.

        Returns:
            int: An integer representing the unique identifier for the current session.

        """
        self.__log_entry("Generate session id")

        #TODO - use incrementing session loaded on start
        session_id = 0
        return session_id
    
    def __generate_job_id(self) -> str:
        """
        Generate and return a unique identifier for the current transcription job.

        Returns:
            str: A string representing the unique identifier for the current transcription job.

        """
        current_job_id = "s" + str(self.session_id) + "j" + str(self.job_id)
        self.job_id+=1

        self.__log_entry("Generated job id: %s" % current_job_id)
        return current_job_id

    def __log_entry(self, entry: str):
        """
        Log the specified entry.

        Args:
            entry (str): A string representing the log entry to be recorded.

        """
        print("TranscribvrServer: " + entry)