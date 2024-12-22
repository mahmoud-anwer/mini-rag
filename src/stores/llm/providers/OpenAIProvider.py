from openai import OpenAI
from utils.logger import logger
from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums

# pylint: disable=too-many-instance-attributes
class OpenAIProvider(LLMInterface):
    """
    A provider class for interacting with OpenAI's API, implementing the LLMInterface.

    This class is responsible for setting up the OpenAI client, generating text, and embedding text
    using the specified models. It also manages configuration parameters such as maximum characters,
    output tokens, and temperature for generation.

    Attributes:
        api_key (str): The API key to authenticate with OpenAI's API.
        api_url (str, optional): The base URL for the OpenAI API (defaults to None).
        default_input_max_characters (int): The default maximum number of input characters (default is 1000).
        default_generation_max_output_tokens (int): The default maximum number of tokens for output generation
                                                    (default is 1000).
        default_generation_temperature (float): The default temperature for controlling randomness in generation
                                                (default is 0.1).
        generation_model_id (str, optional): The ID of the generation model to use (default is None).
        embedding_model_id (str, optional): The ID of the embedding model to use (default is None).
        embedding_size (int, optional): The size of the embedding (default is None).
        client (OpenAI): An instance of the OpenAI API client for making requests.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        """
        Initializes the OpenAIProvider with the provided configuration parameters.

        Args:
            api_key (str): The API key to authenticate with OpenAI's API.
            api_url (str, optional): The base URL for the OpenAI API (default is None).
            default_input_max_characters (int, optional): The maximum number of input characters (default is 1000).
            default_generation_max_output_tokens (int, optional): The maximum number of tokens
                                                                  for output generation (default is 1000).
            default_generation_temperature (float, optional): The temperature for controlling randomness in generation
                                                              (default is 0.1).
        """
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key=self.api_key,
                             base_url=self.api_url if self.api_url and len(self.api_url) else None)

        self.enums = OpenAIEnums

    def set_generation_model(self, model_id: str):
        """
        Sets the model ID for text generation.

        Args:
            model_id (str): The ID of the model to be used for generation.
        """
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Sets the model ID and embedding size for text embedding.

        Args:
            model_id (str): The ID of the model to be used for embedding.
            embedding_size (int): The size of the embedding.
        """
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        """
        Generates text using the OpenAI model based on the provided prompt and other parameters.

        Args:
            prompt (str): The text prompt to generate a response for.
            chat_history (list, optional): A list of previous messages in the chat (default is an empty list).
            max_output_tokens (int, optional): The maximum number of tokens to generate
                                               (default is None, uses the class default).
            temperature (float, optional): The temperature for controlling randomness
                                           (default is None, uses the class default).

        Returns:
            str: The generated text from OpenAI's API response.

        Raises:
            None: Returns None if there is an error in the API response or client setup.
        """
        if not self.client:
            logger.error("OpenAi client was not set")
            return None

        if not self.generation_model_id:
            logger.error("Generations model for OpenAi was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message.content

    def embed_text(self, prompt: str, document_type: str = None):
        """
        Embeds the provided text using OpenAI's embedding model.

        Args:
            prompt (str): The text to embed.
            document_type (str, optional): The type of the document (default is None).

        Returns:
            list: The embedding vector representing the input text.

        Raises:
            None: Returns None if there is an error in the API response or client setup.
        """
        if not self.client:
            logger.error("OpenAi client was not set")
            return None

        if not self.embedding_model_id:
            logger.error("Embedding model for OpenAi was not set")
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=prompt
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            logger.error("Error while embedding text with OpenAI")
            return None

        return response.data[0].embedding

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
