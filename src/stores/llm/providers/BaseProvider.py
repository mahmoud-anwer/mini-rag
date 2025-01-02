from utils.logger import logger
from ..LLMInterface import LLMInterface


class BaseProvider(LLMInterface):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        """
        Initializes the CoHereProvider with the provided API key and optional settings.

        Args:
            api_key (str): The API key for authentication with Cohere.
            api_url (str, optional): The API URL (default is None).
            default_input_max_characters (int, optional): The default maximum input characters (default is 1000).
            default_generation_max_output_tokens (int, optional): The default maximum output tokens (default is 1000).
            default_generation_temperature (float, optional): The default temperature for text generation (default is 0.1).
        """
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

    def set_generation_model(self, model_id: str):
        """
        Sets the generation model ID to be used for text generation.

        Args:
            model_id (str): The model ID to be used for text generation.
        """
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Sets the embedding model ID and its embedding size.

        Args:
            model_id (str): The model ID to be used for embedding text.
            embedding_size (int): The size of the embedding.
        """
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def construct_prompt(self, prompt: str, role: str):
        """
        Constructs a message prompt with the given role and processed text.

        Args:
            prompt (str): The text prompt to process.
            role (str): The role of the user (e.g., "user", "assistant").

        Returns:
            dict: A dictionary with the role and the processed text.
        """
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

    def process_text(self, text: str):
        """
        Processes the input text by trimming it to the default maximum characters.

        Args:
            text (str): The text to process.

        Returns:
            str: The processed text, trimmed to the default maximum characters.
        """
        if self.default_input_max_characters < len(text):
            return text[self.default_input_max_characters:].strip()

        return text.strip()
