from enum import Enum

class LLMEnums(Enum):
    """
    Enum representing different language model platforms.

    Attributes:
        OPENAI: Represents the OpenAI platform.
        COHERE: Represents the Cohere platform.
    """
    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    """
    Enum representing message types or roles for the OpenAI platform.

    Attributes:
        SYSTEM: Represents the system's prompt or setup message.
        USER: Represents the user's input message.
        ASSISTANT: Represents the assistant's (model's) response message.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    """
    Enum representing message types or roles for the CoHere platform.

    Attributes:
        SYSTEM: Represents the system's prompt or setup message.
        USER: Represents the user's input message.
        ASSISTANT: Represents the assistant's (model's) response message.
        DOCUMENT: Represents a document in CoHere.
        QUERY: Represents a search query in CoHere.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):
    """
    Enum representing different types of documents or queries.

    Attributes:
        DOCUMENT: Represents a document.
        QUERY: Represents a search query.
    """
    DOCUMENT = "document"
    QUERY = "query"
