import os
from langchain_openai import AzureChatOpenAI
# Langchain prompting library
from langchain_core.prompts import ChatPromptTemplate
# Langchain utilities
from langchain_core.output_parsers import StrOutputParser


def generate_response_from_openai(messages):
    summarize_model = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version="2024-02-01",
        temperature=0
    )

    SUMMARIZE_PROMPT = """
        you are a helpful assistant.

        User: {input}
    """

    summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
    parser = StrOutputParser()
    chain = summarize_prompt | summarize_model | parser
    response = chain.invoke({"input": messages})
    print(response)
    return response