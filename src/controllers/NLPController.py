from typing import List
import json
from models import Project, DataChunk
from stores.llm import DocumentTypeEnum


class NLPController():
    """
    Controller for handling Natural Language Processing (NLP) tasks related to vector databases.

    Inherits from BaseController and provides methods for interacting with vector databases,
    handling collections, and performing semantic search and text embedding.
    """

    def __init__(self, vectordb_client, generation_client, embedding_client, template_parser):
        """
        Initializes the NLPController instance.

        Args:
            vectordb_client (object): Client for interacting with the vector database.
            generation_client (object): Client for text generation (not used in this class).
            embedding_client (object): Client for generating text embeddings.
        """
        super().__init__()
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        """
        Generates a collection name for the vector database based on the project ID.

        Args:
            project_id (str): The ID of the project to create the collection name for.

        Returns:
            str: The generated collection name.
        """
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self, project: Project):
        """
        Resets the vector database collection associated with the project.

        Deletes the existing collection in the vector database, effectively resetting it.

        Args:
            project (Project): The project whose vector database collection is to be reset.

        Returns:
            object: The response from the vector database client indicating the result of the operation.
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project: Project):
        """
        Retrieves information about the vector database collection associated with the project.

        Args:
            project (Project): The project whose vector database collection info is to be retrieved.

        Returns:
            dict: A dictionary containing the collection information.
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                              chunks_ids: List[int], do_reset: bool = False):
        """
        Indexes the data chunks into the vector database.

        This method processes the chunks, embeds the text into vectors, and inserts them into the
        vector database.

        Args:
            project (Project): The project associated with the data chunks.
            chunks (List[DataChunk]): A list of DataChunk objects containing the text to be indexed.
            chunks_ids (List[int]): A list of chunk IDs to associate with the indexed data.
            do_reset (bool): A flag indicating whether to reset the collection before indexing. Defaults to False.

        Returns:
            bool: Returns True if the indexing operation is successful.
        """
        # Step 1: Get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # Step 2: Prepare texts, metadata, and vectors
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        vectors = [
            self.embedding_client.embed_text(prompt=text,
                                             document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # Step 3: Create collection if it doesn't exist
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # Step 4: Insert data into the vector database
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):
        """
        Performs a semantic search on the vector database collection for the given project.

        Embeds the query text into a vector and searches the collection for similar items.

        Args:
            project (Project): The project associated with the vector database collection to search.
            text (str): The query text to be searched.
            limit (int): The maximum number of results to return. Defaults to 10.

        Returns:
            dict or bool: A dictionary of results if any matches are found, or False if no results are found.
        """
        # Step 1: Get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # Step 2: Embed the query text into a vector
        vector = self.embedding_client.embed_text(prompt=text,
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        # Step 3: Perform the semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results

    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        answer = full_prompt = chat_history = None

        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history

        # Step2: construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        # documents_prompts = []
        # for idx, doc in enumerate(retrieved_documents):
        #     documents_prompts.append(
        #         self.template_parser.get("rag", "document_prompt", {
        #             "doc_num": idx + 1,
        #             "chunk_text": doc.text
        #         })
        #     )

        # comprehension list
        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                "doc_num": idx + 1,
                "chunk_text": doc.text
            })
            for idx, doc in enumerate(retrieved_documents)
        ])


        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
            })

        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value
            )
        ]

        full_prompt = "\n\n".join([documents_prompts, footer_prompt])

        answer = self.generation_client.generate_text(prompt=full_prompt, chat_history=chat_history)

        return answer, full_prompt, chat_history
