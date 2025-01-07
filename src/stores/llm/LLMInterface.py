from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """
    Abstract base class for interacting with language models.

    Provides the structure for classes implementing various language model APIs (e.g., OpenAI, Cohere).
    Concrete classes should define the actual behavior for setting models, generating text,
    embedding text, and constructing prompts.
    """

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Sets the model used for text generation.

        Args:
            model_id (str): The ID of the model to be used for text generation.
        """

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Sets the model used for generating text embeddings.

        Args:
            model_id (str): The ID of the model to be used for text embedding.
            embedding_size (int): The desired embedding size.
        """

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = None, max_output_tokens: int = None,
                      temperature: float = None):
        """
        Generates text based on the provided prompt.

        Args:
            prompt (str): The text prompt to generate text from.
            chat_history (list, optional): A list of previous interactions to maintain context.
            max_output_tokens (int, optional): The maximum number of tokens to generate.
            temperature (float, optional): Controls the randomness of the output (0.0 for deterministic, 1.0 for creative).

        Returns:
            str: The generated text based on the prompt.
        """

    @abstractmethod
    def embed_text(self, prompt: str, document_type: str = None):
        """
        Embeds the provided text or document.

        Args:
            prompt (str): The text to embed.
            document_type (str, optional): Specifies the type of document (e.g., 'query', 'document').

        Returns:
            list: The embedding vector representing the text.
        """

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """
        Constructs a formatted prompt based on the role.

        Args:
            prompt (str): The base prompt.
            role (str): The role of the entity interacting with the model (e.g., 'system', 'user', 'assistant').

        Returns:
            str: The formatted prompt ready for the model.
        """
