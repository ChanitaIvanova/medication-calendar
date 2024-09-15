from .openai_service import OpenAIService
import json
from .file_reader_service import FileReaderService
from werkzeug.utils import secure_filename
import os

class MedicationService:

    def parse_medication_data(self, file):
        # Custom prompt to extract medication data
        prompt = (
            "You are an assistant the will recieve information on medication, that should parse the information and extract the medication data in the follwoing fields as json: "
            "name, contents, sideEffects, objective, dosageSchedule."
            "Each of those fields should be a free text."
            "The returned object should contain only those five properties."
            "The returned value should be a valid json format with no new lines or any thext before or after the json output."
            "Translate to English if necessary.\n"
        )

        # Read the file content
        try:
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            print(file_extension)
            file_content = FileReaderService.read_file(file, file_extension)

            # Use OpenAIService to get the response
            openai_service = OpenAIService()
            response = openai_service.run(prompt, file_content);

            # Assuming the response is in JSON format
            medication_data = json.loads(response)
            return medication_data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file was not found.")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {str(e)}")