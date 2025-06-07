from openai import OpenAI
from dotenv import load_dotenv
import os

preresponce_id = None
def createTextResponse(input_massage):
    global preresponce_id
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    GPTclient = OpenAI()

    if preresponce_id:
        response = GPTclient.responses.create(
        model="gpt-4.1 mini",
        instructions="日本語,口語調,100文字以内",
        input= input_massage,
        max_output_tokens=400,
        temperature=0.3,
        previous_response_id = preresponce_id
        )
        preresponce_id = response.id

    else:
        response = GPTclient.responses.create(
            model="gpt-4.1",
            instructions="日本語,口語調,100文字以内",
            input= input_massage,
            max_output_tokens=400,
            temperature=0.3,
        )
        preresponce_id = response.id

    if response.error != None:
        return response.error
    
    print(preresponce_id)
    return response.output_text