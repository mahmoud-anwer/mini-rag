from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider


class LLMProviderFactory:
    """
    A factory class to create instances of different LLM (Large Language Model) providers.

    This class is responsible for initializing and returning the appropriate provider
    instance based on the provided configuration and the desired provider type.

    Attributes:
        config (dict): A dictionary containing the necessary configuration for LLM providers.
    """
    def __init__(self, config: dict):
        """
        Initializes the LLMProviderFactory with the provided configuration.

        Args:
            config (dict): A dictionary containing the necessary configuration values for LLM providers.
        """
        self.config = config

    def create(self, provider: str):
        """
        Creates and returns the appropriate provider instance based on the given provider name.

        Args:
            provider (str): The name of the provider to create (e.g., "OPENAI", "COHERE").

        Returns:
            OpenAIProvider | CoHereProvider: The corresponding provider instance, or None if the provider is invalid.

        Raises:
            ValueError: If the provider is not supported or is invalid.
        """
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        return None
