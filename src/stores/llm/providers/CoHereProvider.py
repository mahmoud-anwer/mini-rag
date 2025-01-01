import cohere
from utils.logger import logger
from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum

# pylint: disable=too-many-instance-attributes
class CoHereProvider(LLMInterface):
    """
    CoHereProvider is a provider class for interacting with the Cohere API.
    It provides methods to generate text and embed text using Cohere models.
    """

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

        self.client = cohere.ClientV2(api_key=self.api_key)

        self.enums = CoHereEnums

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

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        """
        Generates text based on the provided prompt using the set generation model.

        Args:
            prompt (str): The prompt to generate text from.
            chat_history (list, optional): A history of the chat to provide context (default is an empty list).
            max_output_tokens (int, optional): The maximum number of tokens for the output (default is None, uses default).
            temperature (float, optional): The temperature setting for randomness in generation
                                           (default is None, uses default).

        Returns:
            str: The generated text.
        """
        if not self.client:
            logger.error("OpenAi client was not set")
            return None

        if not self.generation_model_id:
            logger.error("Generations model for OpenAi was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            temperature=temperature,
            max_tokens=max_output_tokens
        )

        if not response or not response.text:
            logger.error("Error while generating text with CoHere")
            return None

        return response.choices[0].message["content"]

    def embed_text(self, prompt: str, document_type: str = None):
        """
        Embeds the provided text prompt using the set embedding model.

        Args:
            prompt (str): The text to be embedded.
            document_type (str, optional): The type of document (default is None, uses the default type).

        Returns:
            list: The embedding of the text.
        """
        if not self.client:
            logger.error("OpenAi client was not set")
            return None

        if not self.embedding_model_id:
            logger.error("Embedding model for OpenAi was not set")
            return None

        input_type = CoHereEnums.DOCUMENT

        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnums.QUERY

        response = self.client.embed(
            texts=[self.process_text(prompt)],
            model=self.embedding_model_id,
            input_type=input_type,
            embedding_types=['float']
        )

        if not response or not response.embeddings or not response.embeddings.float_:
            logger.error("Error while embedding text with CoHere")
            return None

        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        """
        Constructs a prompt for use in communication with the Cohere model.

        Args:
            prompt (str): The text prompt.
            role (str): The role of the entity providing the prompt.

        Returns:
            dict: A dictionary representing the structured prompt.
        """
        return {
            "role": role,
            "text": self.process_text(prompt)
        }

    def process_text(self, text: str):
        """
        Processes the text to ensure it does not exceed the maximum input length.

        Args:
            text (str): The text to process.

        Returns:
            str: The processed text.
        """
        if self.default_input_max_characters < len(text):
            return text[self.default_input_max_characters:].strip()

        return text.strip()
