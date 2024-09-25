from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def get_dynamodb_chat_history(session_id: str):
    return DynamoDBChatMessageHistory(
        table_name="waf_conversation_history", 
        session_id=session_id
    )

# Assuming you have defined summarize_prompt, model, and parser

# Create the base chain
chain = summarize_prompt | model | parser

def create_historical_chain(chain, agent_type):
    if agent_type == 'summarize':
        return RunnableWithMessageHistory(
            chain,
            get_dynamodb_chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
    else:
        # Return the original chain or handle other agent types as needed
        return chain

def process_messages(session_id: str, messages: str, agent_type: str = 'summarize'):
    config = {"configurable": {"session_id": session_id}}
    
    historical_chain = create_historical_chain(chain, agent_type)
    
    response = historical_chain.invoke({"input": messages}, config)
    
    return response

# Usage example:
# session_id = "user123"
# messages = "What is the capital of France?"
# response = process_messages(session_id, messages)
# print(response)