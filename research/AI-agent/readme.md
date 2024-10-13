powertool:
Parser (Pydantic)、Logger、Tracer、 APIGatewayHttpResolver、Capturing cold start metric
https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#api-gateway-http-api

terraform:
build api use the openAPI file


System flow draft https://drive.google.com/file/d/1G7fXOMF86Vh2WWLtih_Lwx9DczoYABMs/view?usp=sharing (use drawio)
Langchain + LLM + OpenSearch Vector + dynamoDB (for chat data/session data) reference https://www.youtube.com/watch?v=soZQ9crG2kk&list=PLhr1KZpdzukdBBUx1LHR8yPNQa5ZTuWYd&index=4

Google custom search api https://developers.google.com/custom-search/v1/introduction

Langchain https://python.langchain.com/v0.2/docs/tutorials/https://python.langchain.com/v0.1/docs/integrations/tools/awslambda/

Bedrock for embedding
https://python.langchain.com/v0.2/docs/integrations/text_embedding/bedrock/
Bedrock as chat model
https://python.langchain.com/v0.2/docs/integrations/chat/bedrock/
Bedrock direct from JSON API
https://medium.com/@codingmatheus/sending-images-to-claude-3-using-amazon-bedrock-b588f104424f
Document loaders
https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/
OpenSearch as retriever
https://python.langchain.com/v0.2/docs/integrations/vectorstores/opensearch/#using-aos-amazon-opensearch-service
Retriever as tool/Custom tools/Agent
https://python.langchain.com/v0.1/docs/use_cases/tool_use/quickstart/
https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/#retrieval-tool
Memory management
https://python.langchain.com/v0.1/docs/use_cases/chatbots/memory_management/#summary-memory
GPT-4o with langchain multimodal input (should work but doesnt work)
https://billtcheng2013.medium.com/azure-openai-gpt-4o-with-langchain-ad2b9375a6ee
AI Flow, so far
https://drive.google.com/file/d/1khYUPhrSFZUXX6wp09f4YtKaAcyINgS8/view?usp=sharing


## learning resources
- [What is AWS Lambda](https://serverlessland.com/content/service/lambda/guides/aws-lambda-fundamentals/what-is-aws-lambda)
- [Developer Roadmaps](https://roadmap.sh/roadmaps)
- [Serverless 101: Understanding the serverless services](https://serverlessland.com/learn/serverless-101)
- [What is serverless development?](https://docs.aws.amazon.com/serverless/latest/devguide/welcome.html)
- [AWS Lambda Cookbook — Part 1 — Logging Best Practices with CloudWatch Logs and Powertools for AWS](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-elevate-your-handler-s-code-part-1-logging)
- [RAG on LLM through Intelligent Search Solution Workshop V2 (workshops.aws)](https://catalog.us-east-1.prod.workshops.aws/workshops/486e5ddd-b414-4e7f-9bfd-3884a89353e3/en-US/02preinstall/21preinstall)