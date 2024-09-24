import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import prompt


def generate_response_from_openai(messages, promptType, CVE_context=None):
   summarize_model = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version="2024-02-01",
        temperature=0
   )
   if promptType == "cve":
      SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} CVEinfo: {CVE_context} User: {messages}"
   else:
      SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} User: {messages}"
   summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
   parser = StrOutputParser()
   chain = summarize_prompt | summarize_model | parser
   response = chain.invoke({"input": summarize_prompt})
   return response