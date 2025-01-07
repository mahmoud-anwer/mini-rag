from openai import OpenAI
from utils.logger import logger
from ..LLMEnums import OpenAIEnums
from .BaseProvider import BaseProvider


# pylint: disable=too-many-instance-attributes
class OpenAIProvider(BaseProvider):
    """
    A provider class for interacting with OpenAI's API, implementing the LLMInterface.

    This class is responsible for setting up the OpenAI client, generating text, and embedding text
    using the specified models. It also manages configuration parameters such as maximum characters,
    output tokens, and temperature for generation.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        super().__init__(api_key, api_url, default_input_max_characters,
                         default_generation_max_output_tokens, default_generation_temperature)
        self.client = OpenAI(api_key=api_key,
                             base_url=api_url if api_url and len(api_url) else None)
        self.enums = OpenAIEnums

    def generate_text(self, prompt: str, chat_history: list = None, max_output_tokens: int = None,
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
        # pylint: disable=duplicate-code
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
