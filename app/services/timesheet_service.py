from .openai_service import OpenAIService
import json

class TimesheetService:
        
    def build_timesheet(self, medications, start_date_str, end_date_str):
        # Custom prompt to extract medication data
        prompt = (
            "You are an assistant the will recieve list of medications, you should use the medication information to build a timesheet for how a user should take the medications."
            "The information will contain a start and end dates for the period where the medications should be taken and a list of medications with information for dosage, contents, side effects, objective."
            "Pay special attention to the dosage for each medication, at what time it should be taken, should it be taken without or with food, should it be taken with fluids or no."
            "Use this information to build a timesheet for each medication. Pay attention for how to combine those medications and add any relative information to the advise property for each medication where needed."
            "Have in mind that most peope are awake from 08:00 until about 22:00 and make the schedule accordingly unless the medication should be taken during sleep hour or at exact time inttervals."
            "Return the timesheet with follwoing fields as json: "
            "id, name, dates, dosage, advise."
            "Each of those fields should be a free text."
            "The returned object should contain only those five properties."
            "The id - should contain the same id as in the provided in information and should match the medication"
            "The dates fields should be a list of dates with times when the medication should be taken in the provided period. The format should always be '%Y-%m-%dT%H:%M:%S'"
            "The dosage should be a free text with information on how and how many dosages should be taken from this medication"
            "The returned value should be a valid json format with no new lines or any thext before or after the json output.\n"
        )

        # Create the JSON string with medications, start_date, and end_date
        data = {
            "medications": medications,
            "start_date": start_date_str,
            "end_date": end_date_str
        }
        
        data_json = json.dumps(data)
        response = ""

        # Use OpenAIService to get the response
        try:
            openai_service = OpenAIService()
            response = openai_service.run(prompt, data_json)
            
            # Assuming the response is in JSON format
            timesheet = json.loads(response)
            return timesheet
        except json.JSONDecodeError:
            raise ValueError("The response from OpenAIService is not a valid JSON. Instead it was: " + response)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {str(e)}")