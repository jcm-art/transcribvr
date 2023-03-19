import sys
import os

from transcription_server import TranscribvrServer

class TranscribvrCommandLineClient(object):
    """
    A class that sends audio files to the transcription server class for transcription processing
    """

    def __init__(self, sysArgs):
            """
            Constructor for the TranscribvrCommandLineClient class; class receives system arguments
            from the command line with audio file names and sends them to the transcription server 

            Args:
            None.

            Returns:
            None.

            """
            self.__log_entry("Initializing TranscribvrCommandLineClient")
            self.__log_entry(f"Received {len(sysArgs)} inputs for transcription service")

            #Initializes TranscribvrServer and empty request
            ts = TranscribvrServer()
            transcription_request=[]

            #Gets absolute path for all requests
            for i, arg in enumerate(sysArgs):
                request_abs_path = os.path.abspath(arg)
                transcription_request.append(request_abs_path)
                self.__log_entry(f"File {i} is {request_abs_path}")
            
            self.__log_entry("Sending requests to TranscribvrServer")
            ts.assign_transcription_request(transcription_request)


    def __log_entry(self, entry: str):
        """
        Log the specified entry.

        Args:
            entry (str): A string representing the log entry to be recorded.

        """
        print("TranscribvrCommandLineClient: " + entry)

if __name__ == "__main__":
    TranscribvrCommandLineClient(sys.argv[1:])