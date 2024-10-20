import configparser
from openai import OpenAI
import logging

class OpenAIService:
    """
    A service class to interact with OpenAI's API.
    
    This class handles loading the API key, initializing the OpenAI client, and making requests to the API.
    """
    def __init__(self, config_path='config.dev.ini'):
        """
        Initialize the OpenAIService instance.

        :param config_path: Path to the configuration file containing the OpenAI API key.
        :type config_path: str
        :raises ValueError: If the API key cannot be loaded from the configuration file.
        :raises ConnectionError: If the OpenAI client cannot be initialized.
        """
        try:
            self.api_key = self._load_api_key(config_path)
        except (configparser.Error, KeyError) as e:
            logging.error(f"Error loading API key from config file: {e}")
            raise ValueError("Failed to load API key from configuration file.")
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            logging.error(f"Error initializing OpenAI client: {e}")
            raise ConnectionError("Failed to initialize OpenAI client.")

    def _load_api_key(self, config_path):
        """
        Load the OpenAI API key from the configuration file.

        :param config_path: Path to the configuration file.
        :type config_path: str
        :return: The OpenAI API key.
        :rtype: str
        :raises KeyError: If the 'OpenAI' section or 'api_key' key is missing in the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        return config['OpenAI']['api_key']

    def run(self, assistant_prompt, query):
        """
        Run a chat model with the provided assistant prompt and user query.

        :param assistant_prompt: The system prompt to guide the assistant's behavior.
        :type assistant_prompt: str
        :param query: The user's query or message.
        :type query: str
        :return: The response content from the chat model.
        :rtype: str
        """
        messages = [
            {"role": "system", "content": assistant_prompt},
            {"role": "user", "content": query}
        ]
        return self.__run_chat_model(messages)

    def __run_chat_model(self, messages):
        """
        Run the chat model with the provided messages.

        :param messages: A list of message dictionaries containing roles and content.
        :type messages: list
        :return: The response content from the chat model.
        :rtype: str
        :raises RuntimeError: If the API call fails.
        """
        try:
            response = self.client.chat.completions.create(model="gpt-4o-mini",
            messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during OpenAI API call: {e}")
            raise RuntimeError("Failed to get response from OpenAI API.")
