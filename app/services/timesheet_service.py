from .openai_service import OpenAIService
import json
import requests.exceptions
import logging

class TimesheetService:
    """
    A service class for building a timesheet based on medication information using OpenAI's API.
    
    This service takes medication data along with a start and end date to generate a schedule (timesheet) for when the medications should be taken.
    """
    def __init__(self):
        """
        Initialize the TimesheetService instance.

        This method creates an instance of OpenAIService to be used for generating timesheets.
        """
        # Instantiate OpenAIService once to avoid creating multiple instances
        self.openai_service = OpenAIService()
        
    def build_timesheet(self, medications, start_date_str, end_date_str):
        """
        Build a timesheet for taking medications within a specified time frame.

        This method uses OpenAI's API to generate a timesheet for a list of medications, considering dosage, timing, and any specific requirements.

        :param medications: A list of medications with relevant information (e.g., dosage, contents, side effects, objective).
        :type medications: list
        :param start_date_str: The start date of the period for taking the medications (in YYYY-MM-DD format).
        :type start_date_str: str
        :param end_date_str: The end date of the period for taking the medications (in YYYY-MM-DD format).
        :type end_date_str: str
        :return: A dictionary containing the timesheet with fields: id, name, dates, dosage, advise.
        :rtype: dict
        :raises ValueError: If the response from OpenAIService is not valid JSON or if it is missing required fields.
        :raises ConnectionError: If a network error occurs while contacting OpenAIService.
        :raises IOError: For any other errors that occur while processing the request.
        """
        
        prompt = (
            "You are an assistant that will receive a list of medications, you should use the medication information to build a timesheet for how a user should take the medications."
            "The information will contain start and end dates for the period during which the medications should be taken and a list of medications with information for dosage, contents, side effects, objective."
            "For each create a timesheet based on the dosage information for the medication - do not exceed the start and end date provided, if in the medication information there is a period that should not be exceeded- do not exceed this one as well, "
            "if there is a specific schema for taking the medication buld the schedule based on it and do not exceed the days even if the start and end date for the timesheet have wider range. "
            "Consider the person taking the medication as an adult less than 65 years old"
            "Keep in mind that most people are awake from 08:00 until about 22:00 and make the schedule accordingly unless the medication should be taken during sleep hours or at exact time intervals."
            "Pay special attention to the dosage for each medication, at what time it should be taken, should it be taken without or with food, should it be taken with fluids or not."
            "Pay attention to how to combine those medications and add any relevant information to the advise property for each medication where needed."
            "Return the timesheet with the following fields as json: "
            "The top level field should me called 'medications' and should contain the same medications as the provided for each of them the following fields should be present:"
            "id, name, dates, dosage, advise."
            "Each of those fields should be free text."
            "For each medication the returned object should contain only those five properties."
            "The id - should contain the same id as provided in the information and should match the medication."
            "The name - should contain the same name as provided in the information and should match the medication."
            "The dates field should be a list of dates with times when the medication should be taken in the provided period. The format should always be '%Y-%m-%dT%H:%M:%S'. Do not skip dates and times even if the period is long"
            "The dosage should be free text with information on how and how many dosages should be taken from this medication."
            "The advise should be free text with information for the medication in case there are some specifics when taking it."
            "The returned value should be a valid json format with no new lines or any text before or after the json output.\n"
        )
        
        # prompt = (
        #     "You are an assistant that will receive a list of medications, you should use the medication information to build a timesheet for how a user should take the medications."
        #     "The information will contain start and end dates for the period during which the medications should be taken and a list of medications with information for dosage, contents, side effects, objective."
        #     "Pay special attention to the dosage for each medication, at what time it should be taken, should it be taken without or with food, should it be taken with fluids or not."
        #     "Use this information to build a timesheet for each medication."
        #     "Pay attention to how to combine those medications and add any relevant information to the advise property for each medication where needed."
        #     "Pay attention to any specific schemas for taking the medications when building the time sheet and do not exceed the prescribed time even if the start and end date provided are longer"
        #     "Keep in mind that most people are awake from 08:00 until about 22:00 and make the schedule accordingly unless the medication should be taken during sleep hours or at exact time intervals."
        #     "Return the timesheet with the following fields as json: "
        #     "The top level field should me called 'medications' and should contain the same medications as the provided for each of them the following fields should be present:"
        #     "id, name, dates, dosage, advise."
        #     "Each of those fields should be free text."
        #     "The returned object should contain only those five properties."
        #     "The id - should contain the same id as provided in the information and should match the medication."
        #     "The name - should contain the same name as provided in the information and should match the medication."
        #     "The dates field should be a list of dates with times when the medication should be taken in the provided period. The format should always be '%Y-%m-%dT%H:%M:%S'."
        #     "The dosage should be free text with information on how and how many dosages should be taken from this medication."
        #     "The advise should be free text with information for the medication in case there are some specifics when taking it."
        #     "The returned value should be a valid json format with no new lines or any text before or after the json output.\n"
        # )

        data = {
            "medications": medications,
            "start_date": start_date_str,
            "end_date": end_date_str
        }
        
        # data = {
        #     "timesheet": [
        #         {
        #             "dates": [
        #                 {
        #                     "date": "2024-01-10",
        #                     "times": [
        #                         {
        #                             "time": "08:00:00",
        #                             "medications": [
        #                                 {
        #                                     "id": "989898dfsf2332",
        #                                     "name": "Test Medication",
        #                                     "dosage": "2 tablets",
        #                                     "advise": "Should be taken with a lot of liquids, in case of stomache ache skip the next tablets for the day"
        #                                 },
        #                                 {
        #                                     "id": "989898dfsf233sdsad2",
        #                                     "name": "Test Medication 2",
        #                                     "dosage": "1 tablets",
        #                                     "advise": "Should be taken with after or during meals"
        #                                 }
        #                             ]
        #                         },
        #                         {
        #                             "time": "09:00:00",
        #                             "medications": [
        #                                 {
        #                                     "id": "989898dfsf2332sddas",
        #                                     "name": "Test Medication3",
        #                                     "dosage": "1 tablets",
        #                                     "advise": "Should NOT be taken with other medications. Should be duration of at least 1 hour between medications"
        #                                 },
        #                             ]
        #                         }
        #                     ]
        #                 }
        #             ]
                    
        #         }],
        #     "start_date": start_date_str,
        #     "end_date": end_date_str
        # }
        
        
        data_json = json.dumps(data)
        response = ""

        try:
            response = self.openai_service.run(prompt, data_json)
            
            timesheet = json.loads(response)
            return timesheet
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {str(e)}. Response: {response}")
            raise ValueError("The response from OpenAIService is not a valid JSON. Instead it was: " + response)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"A network error occurred while contacting OpenAIService: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise IOError(f"An error occurred while processing the request: {str(e)}")
