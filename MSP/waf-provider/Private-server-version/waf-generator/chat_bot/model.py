import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import prompt
from cve_retriever import searchCVE
from cve_query import parse_user_input, search_cve, parse_cve_results

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
            SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} CVEinfo: {CVE_context}\n\nConversation History:\n{history_str}\nUser: {messages}"
            summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
            parser = StrOutputParser()
            chain = summarize_prompt | summarize_model | parser
            response = chain.invoke({"input": summarize_prompt})
         else:
            response = response.replace("CVE_QUERY", "")
      except Exception as e:
         print(e)
      


   # if promptType == "cve":
   #    SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} CVEinfo: {CVE_context}\n\nConversation History:\n{history_str}\nUser: {messages}"
   # else:
   #    SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)}\n\nConversation History:\n{history_str}\nUser: {messages}"

   
   print(response)
   return response