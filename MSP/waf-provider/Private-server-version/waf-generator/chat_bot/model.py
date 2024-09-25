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
from prompt import RULE_PROMPT, PROFESSIONALISM_PROMPT, CVE_PROMPT, JSON_GENERATOR_PROMPT


def get_dynamodb_chat_history(session_id: str):
   return DynamoDBChatMessageHistory(
      table_name="waf_conversation_history", 
      session_id=session_id
    )

def create_historical_chain(chain, agent_type):
   # if agent_type == 'summarize':
      return RunnableWithMessageHistory(
            chain,
            get_dynamodb_chat_history,
            input_messages_key="input", 
            history_messages_key="chat_history", # check input key "chat_history"
      )
   # elif agent_type == 'json_generator':
   #    ## here
   #    return None
   # elif agent_type == 'cve':
   #    ## here
   #    return None

def process_messages(session_id: str, messages: str, agent_type: str = 'summarize', chain=None):
   config = {"configurable": {"session_id": session_id}} 
   historical_chain = create_historical_chain(chain, agent_type)

   chat_history = get_dynamodb_chat_history(session_id)
   history_messages = chat_history.messages
   chain_input = {
        "input": messages,
        "chat_history": history_messages
    }

   response = historical_chain.invoke(chain_input, config)
   chat_history.add_user_message(messages)
   chat_history.add_ai_message(response)
   print(chat_history.messages)
    
   return response

tracer = Tracer()

@tracer.capture_method
def generate_response_from_openai(messages, promptType, CVE_context=None, history=None):
   summarize_model = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version="2024-02-01",
        temperature=0
   )

   professionalism_prompt = ChatPromptTemplate.from_template(PROFESSIONALISM_PROMPT)
   parser = StrOutputParser()
   chain = professionalism_prompt | summarize_model | parser
   session_id = 123 # for test
   response = process_messages(session_id, messages, chain=chain)

   
   # if "CVE_REQUEST" in response:
   #    try:
   #       params = parse_user_input(messages)
   #       if params['cve_id']:
   #          results = str(searchCVE(params['cve_id']))
   #          if results:
   #             SUMMARIZE_PROMPT = f"{prompt.prompt_retriever(promptType)} CVEinfo: {results}\n\nConversation History:\n{history_str}\nUser: {messages}"
   #             summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
   #             parser = StrOutputParser()
   #             chain = summarize_prompt | summarize_model | parser
   #             response = chain.invoke({"input": summarize_prompt})
   #       else:
   #          response = response.replace("CVE_QUERY", "")
   #    except Exception as e:
   #       print(e)
   # if "JSON_REQUEST" in response:
   #    try:
   #       SUMMARIZE_PROMPT = f"{prompt.prompt_retriever('json')}\n\nConversation History:\n{history_str}\nUser: {messages}"
   #       summarize_prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
   #       parser = StrOutputParser()
   #       chain = summarize_prompt | summarize_model | parser
   #       response = chain.invoke({"input": summarize_prompt})
   #    except Exception as e:
   #       print(e)

   # if "RULE_PACKAGE_DEPLOY" in response:
   #    target_rule_package = response[response.find("RULE_PACKAGE_DEPLOY")+18:]
   #    rule_json = other_rule_retriever(target_rule_package)
   #    response = str(rule_json)
   #    # response = response.replace("RULE_PACKAGE_DEPLOY", f"\n{rule_json}")
   
   return response
