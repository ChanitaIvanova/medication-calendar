from .openai_service import OpenAIService
import json
from json.decoder import JSONDecodeError
from .file_reader_service import FileReaderService
from werkzeug.utils import secure_filename
import os

class MedicationService:
    """
    A service class to handle the extraction of medication data from a file using OpenAI's API.
    
    This service reads a file, processes it through OpenAI's API, and extracts the required medication information.
    """
    def __init__(self):
        """
        Initialize the MedicationService instance.

        This method creates an instance of the OpenAIService to be used for processing medication data.
        """
        self.openai_service = OpenAIService()

    def parse_medication_data(self, file):
        """
        Parse medication data from a given file.

        This method reads the content of the file, sends it to OpenAI for processing, and extracts the medication data in JSON format.

        :param file: The file containing medication information to be processed.
        :type file: FileStorage (werkzeug.datastructures.FileStorage)
        :return: A dictionary containing extracted medication data with fields: name, contents, sideEffects, objective, dosageSchedule.
        :rtype: dict
        :raises FileNotFoundError: If the file is not found.
        :raises ValueError: If the response from OpenAI cannot be parsed as JSON or if there is an issue with the response data.
        :raises IOError: For any other errors that occur while reading the file or processing the data.
        """
        prompt = (
            "You are an assistant that will receive information on medication, that should parse the information and extract the medication data in the following fields as json: "
            "name, contents, sideEffects, objective, dosageSchedule."
            "Each of those fields should be a free text."
            "The returned object should contain only those five properties."
            "The returned value should be a valid json format with no new lines or any text before or after the json output."
            "Translate to English if necessary.\n"
        )

        try:
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            file_content = FileReaderService.read_file(file, file_extension)

            response = self.openai_service.run(prompt, file_content)

            medication_data = json.loads(response)
            return medication_data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file was not found.")
        except JSONDecodeError as e:
            raise ValueError(f"Failed to parse the response from OpenAI as JSON: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {str(e)}")
