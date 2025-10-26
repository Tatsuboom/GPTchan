from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
GPTclient = OpenAI()
preresponce_id = None

def createTextResponse(input_massage):
    global preresponce_id

    rollfile = open('SubRolls.txt', 'r', encoding='utf-8')
    rolltext = rollfile.read()

    if preresponce_id:
        print("Start")
        response = GPTclient.responses.create(
        model="gpt-4o-mini",
        instructions="日本語,口語調,100文字以内" + rolltext,
        input=input_massage,
        max_output_tokens=120,
        temperature=0.2,
        previous_response_id = preresponce_id
        )
        preresponce_id = response.id
        print("End")

    else:
        response = GPTclient.responses.create(
            model="gpt-4o-mini",
            instructions="日本語,口語調,100文字以内" + rolltext,
            input=input_massage,
            max_output_tokens=120,
            temperature=0.2,
        )
        preresponce_id = response.id

    rollfile.close()

    if response.error != None:
        return response.error
    
    return response.output_text