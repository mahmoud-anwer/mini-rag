from enum import Enum

class VectorDBEnums(Enum):
    """
    Enum for different types of vector databases.
    """
    QDRANT = "QDRANT"

class DistanceMethodEnums(Enum):
    """
    Enum for different distance calculation methods used in vector search.
    """
    COSINE = "cosine"
    DOT = "dot"
