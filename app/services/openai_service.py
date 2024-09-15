import configparser
from openai import OpenAI


class OpenAIService:
    def __init__(self, config_path='config.dev.ini'):
        self.api_key = self._load_api_key(config_path)
        self.client = OpenAI(api_key=self.api_key)

    def _load_api_key(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config['OpenAI']['api_key']

    def run(self, assistant_prompt, query):
        messages = [
            {"role": "system", "content": assistant_prompt},
            {"role": "user", "content": query}
        ]
        return self.__run_chat_model(messages)

    def __run_chat_model(self, messages):
        response = self.client.chat.completions.create(model="gpt-4o-mini",
        messages=messages)
        return response.choices[0].message.content