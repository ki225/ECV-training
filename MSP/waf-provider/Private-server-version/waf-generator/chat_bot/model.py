import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import prompt
from cve_query import parse_user_input, searchCVE

def generate_response_from_openai(messages, promptType, CVE_context=None, history=None):
   summarize_model = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version="2024-02-01",
        temperature=0
   )
   history_str = ""
   if history:
      for msg in history:
         history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"

   SUMMARIZE_PROMPT = f"{prompt.prompt_retriever('professionalism')}\n\nConversation History:\n{history_str}\nUser: {messages}"
   summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
   parser = StrOutputParser()
   chain = summarize_prompt | summarize_model | parser
   response = chain.invoke({"input": summarize_prompt})

   if "CVE_REQUEST" in response:
      try:
         params = parse_user_input(messages)
         if params['cve_id']:
            results = str(searchCVE(params['cve_id']))
            if results:
               SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} CVEinfo: {results}\n\nConversation History:\n{history_str}\nUser: {messages}"
               summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
               parser = StrOutputParser()
               chain = summarize_prompt | summarize_model | parser
               response = chain.invoke({"input": summarize_prompt})
         else:
            response = response.replace("CVE_QUERY", "")
      except Exception as e:
         print(e)
   if "JSON_REQUEST" in response:
      try:
         SUMMARIZE_PROMPT = f"{prompt.prompt_retriever('json')}\n\nConversation History:\n{history_str}\nUser: {messages}"
         summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
         parser = StrOutputParser()
         chain = summarize_prompt | summarize_model | parser
         response = chain.invoke({"input": summarize_prompt})
      except Exception as e:
         print(e)
   return response