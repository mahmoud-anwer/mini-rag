import os

class TemplateParser:
    """
    A class to parse and manage localized templates based on a specified language.

    Attributes:
        current_path (str): The directory path of the current script.
        default_language (str): The fallback language to use when a specified language is unavailable.
        language (str): The currently set language for parsing templates.
    """

    def __init__(self, language: str = None, default_language='en'):
        """
        Initializes the TemplateParser with a specified language and default fallback language.

        Args:
            language (str, optional): The preferred language. Defaults to None.
            default_language (str): The fallback language. Defaults to 'en'.
        """
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        self.set_language(language=language)

    def set_language(self, language: str):
        """
        Sets the current language for the parser. Falls back to the default language if the specified language
        is unavailable.

        Args:
            language (str): The preferred language to set.

        Raises:
            None: This method handles missing language paths gracefully.
        """
        if not language:
            self.language = self.default_language

        language_path = os.path.join(self.current_path, "locales", language)
        if language and os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group: str, key: str, variables: dict = None):
        """
        Retrieves a template string from the specified group and key, replacing placeholders with values from variables.

        Args:
            group (str): The name of the group (file) containing the template.
            key (str): The key corresponding to the desired template within the group.
            variables (dict, optional): A dictionary of variables to substitute into the template. Defaults to
                an empty dictionary.

        Returns:
            str: The parsed template string with placeholders replaced by variables values, or None if the group or
                key is not found.
        """
        if not group or not key:
            return None

        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language

        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language
        if not os.path.exists(group_path):
            return None

        # Import the group module dynamically
        module = __import__(
            f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist=[group]
        )
        if not module:
            return None

        key_attribute = getattr(module, key)
        return key_attribute.substitute(variables)
