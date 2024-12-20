from string import Template

### RAG PROMPTS

system_prompt = Template("\n".join(["You are called Mini-Rag.",
                 "You are an assistant to generate a response for the user.",
                 "You have to generate response based on the documents provided.",
                 "Ignore the document that are not related to the query."
                ]))

### Document
document_prompt = Template(
        "\n".join([
            "## Document No: $doc_num",
            "### Content: $chunk_text"
        ])
)

### Footer
footer_prompt = Template(
        "\n".join([
            "Based only on the above document, please generate an answer for the user.",
            "## Question:",
            "$query",
            "",
            "## Answer:",
        ])
)
