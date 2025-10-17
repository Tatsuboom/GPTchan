from openai import OpenAI
from dotenv import load_dotenv
import os

preresponce_id = None
def createTextResponse(input_massage):
    global preresponce_id
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    GPTclient = OpenAI()

    rollfile = open('SubRolls.txt', 'r', encoding='utf-8')
    rolltext = rollfile.read()

    if preresponce_id:
        response = GPTclient.responses.create(
        model="gpt-4.1",
        instructions="条件2より条件1を必ず優先すること #条件1「日本語,口語調,100文字以内」条件2「" + rolltext + "」",
        input=input_massage,
        max_output_tokens=400,
        temperature=0.2,
        previous_response_id = preresponce_id
        )
        preresponce_id = response.id

    else:
        response = GPTclient.responses.create(
            model="gpt-4.1",
            instructions="条件2より条件1を必ず優先すること #条件1「日本語,口語調,100文字以内」条件2「" + rolltext + "」",
            input=input_massage,
            max_output_tokens=400,
            temperature=0.2,
        )
        preresponce_id = response.id

    rollfile.close()

    if response.error != None:
        return response.error
    
    return response.output_text