import cohere
from utils.logger import logger
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
from .BaseProvider import BaseProvider

# pylint: disable=too-many-instance-attributes
class CoHereProvider(BaseProvider):
    """
    CoHereProvider is a provider class for interacting with the Cohere API.
    It provides methods to generate text and embed text using Cohere models.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        super().__init__(api_key, api_url, default_input_max_characters,
                         default_generation_max_output_tokens, default_generation_temperature)
        self.client = cohere.ClientV2(api_key=api_key)
        self.enums = CoHereEnums


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
        # pylint: disable=duplicate-code
        if not self.client:
            logger.error("CoHere client was not set")
            return None

        if not self.generation_model_id:
            logger.error("Generations model for CoHere was not set")
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
            logger.error("CoHere client was not set")
            return None

        if not self.embedding_model_id:
            logger.error("Embedding model for CoHere was not set")
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
