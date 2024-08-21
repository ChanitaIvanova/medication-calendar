import configparser
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class OpenAIService:
    def __init__(self, config_path='config.ini'):
        self.api_key = self._load_api_key(config_path)
        self.llm = OpenAI(model_name="gpt4o-mini", api_key=self.api_key)
        self.chain = None

    def _load_api_key(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config['OpenAI']['api_key']

    def add_prompt(self, template):
        prompt = PromptTemplate(template=template, input_variables=["query"])
        self.chain = LLMChain(llm=self.llm, prompt=prompt)

    def add_file_context(self, template, file_path):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            
            context_template = template + f"File content:\n{file_content}\n\nQuery: {{query}}"
            self.add_prompt(context_template)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except IOError:
            raise IOError(f"An error occurred while reading the file {file_path}.")

    def chain_prompt(self, template):
        if not self.chain:
            raise ValueError("Initial prompt not set. Use add_prompt first.")
        
        new_prompt = PromptTemplate(template=template, input_variables=["query"])
        self.chain = self.chain | LLMChain(llm=self.llm, prompt=new_prompt)

    def run(self, query):
        if not self.chain:
            raise ValueError("No prompt set. Use add_prompt first.")
        
        return self.chain.run(query)