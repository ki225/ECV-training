import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from cve_query import parse_user_input, searchCVE
from rule_retriever import cve_rule_retriever, other_rule_retriever
from aws_lambda_powertools import Logger, Tracer
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompt import RULE_CHOICE_PROMPT, PROFESSIONALISM_PROMPT, CVE_PROMPT, JSON_GENERATOR_PROMPT, JSON_OUTPUT_PROMPT, AI_PROMPT, WAF_DESCRIBE_PROMPT
import boto3

dynamodb = boto3.resource("dynamodb")

# primary_key/partition_key is set "SessionId" as default
def get_dynamodb_chat_history(session_id: str):
   return DynamoDBChatMessageHistory(
      table_name="session-test", 
      session_id=session_id,
      primary_key_name="session_id",
    )

def create_historical_chain(chain, agent_type):
      return RunnableWithMessageHistory(
            chain,
            get_dynamodb_chat_history,
            input_messages_key="input", 
            history_messages_key="chat_history", # check input key "chat_history"
      )

def process_messages(session_id: str, messages: str, agent_type: str = 'summarize', chain=None, user_id="123"):
   config = {"configurable": {"session_id": session_id}} 
   historical_chain = create_historical_chain(chain, agent_type)

   chat_history = get_dynamodb_chat_history(session_id)
   history_messages = chat_history.messages
   chain_input = {
        "input": messages,
        "chat_history": history_messages,
        "user_id": user_id
    }

   response = historical_chain.invoke(chain_input, config)
    
   return response

def package_retriever(input_string):
   if "RULE_PACKAGE_DEPLOY" in input_string:
      rule_package_name = input_string.split("RULE_PACKAGE_DEPLOY")[1].strip()
      return rule_package_name
   return None
      

tracer = Tracer()

@tracer.capture_method
def generate_response_from_openai(messages, promptType, CVE_context=None):
   summarize_model = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version="2024-02-01",
        temperature=0
   )

   professionalism_prompt = ChatPromptTemplate.from_template(PROFESSIONALISM_PROMPT)
   parser = StrOutputParser()
   chain = professionalism_prompt | summarize_model | parser
   session_id = "456" # for test
   response = process_messages(session_id, messages, chain=chain)

   prompt = None
   generate = False
   package_id = None
   
   # understand user's need for particular topic
   if "RULE_PACKAGE_DEPLOY" in response:
      prompt = ChatPromptTemplate.from_template(RULE_CHOICE_PROMPT) 
   elif "WAF_DESCRIBE" in response:
      prompt = ChatPromptTemplate.from_template(WAF_DESCRIBE_PROMPT) 
   elif "CVE_QUERY" in response:
      prompt = ChatPromptTemplate.from_template(CVE_PROMPT) 
   elif "JSON_GENERATOR" in response:
      prompt = ChatPromptTemplate.from_template(JSON_GENERATOR_PROMPT) 
   elif "JSON_OUTPUT" in response:
      prompt = ChatPromptTemplate.from_template(JSON_OUTPUT_PROMPT) 
      generate = True
   elif "JSON_RESPONSE" in response:
      return "Waf configuration setting complete."

   # reply to user
   if prompt:
      second_chain = prompt | summarize_model | parser
      final_response = process_messages(session_id, response, chain=second_chain)
      if generate:
         package_id = package_retriever(final_response)
         if package_id is not None:
            config_prompt = ChatPromptTemplate.from_template(JSON_OUTPUT_PROMPT)
            config_chain = config_prompt | summarize_model | parser
            config_response = process_messages(session_id, response, chain=config_chain)
            return config_response
         else:
            return final_response   

      return final_response
   return response