# answer_router.py
from fastapi import APIRouter
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
import json
from langchain_core.output_parsers import StrOutputParser
qq_LLM_router = APIRouter()

@qq_LLM_router.post("/qq")
async def answer(request_data: dict):
    topic = request_data.get("topic")
    words = request_data.get("words")
    context = request_data.get("context")
    
    multiple_input_prompt = PromptTemplate(
        input_variables=["topic", "context","words"] ,
        template=("""
                 "create a JSON object which contains a small excerpt of the given and the context in {words} words. "

                 topic --------
                 {topic}                 
                --------

                 context below -----
                 {context}
                 -------
                
                "Please adhere to this JSON structure in your response" 
                "JSON Object Schema below -----"
                 "description' : "[generated description]"
                 -------
              
                "Do not deviate a lot from the topic and context and try and stick to the word limit".
                """

                )
        
    )
    chat_model = ChatOpenAI(temperature=0.8)
  
    chain =(
            multiple_input_prompt 
            | chat_model 
            | StrOutputParser()
        )


    result = chain.invoke({"topic": topic, "words":words,"context":context})

    response = json.dumps(result)
    
 
    return response
