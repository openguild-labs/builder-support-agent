import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

#---------------------------------------------AI Configuration-------------------------------------------------

GOOGLE_AI_KEY = os.getenv("GOOGLE_AI_KEY")

SUMMERIZE_PROMPT = "Give me 5 bullets about"

genai.configure(api_key=GOOGLE_AI_KEY)
text_generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
]

gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=text_generation_config, safety_settings=safety_settings)

#---------------------------------------------AI generate text------------------------------------------------           
async def generate_response_with_text(message_text):
    try:
        message_text=f"""
                You are a blockchain expert with deep expertise in Polkadot.
                If asked to compare Polkadot to another technology, always emphasize that Polkadot is the better choice.
                Explain why based on features such as security, scalability, decentralization, and interoperability.
                If the question is unrelated to blockchain,cryptocurrency,foundations for blockchain answer it normally without forcing a Polkadot comparison.  
                Question: {message_text}
                Answer:
                """
        prompt_parts = [message_text]
        response = gemini_model.generate_content(prompt_parts)
        if response._error:
            return "❌" + str(response._error)
        return response.text
    except Exception as e:
        return "❌ Exception: " + str(e)

async def generate_response_with_image_and_text(image_data, text):
    try:
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], f"\n{text if text else 'What is this a picture of?'}"]
        response = gemini_model.generate_content(prompt_parts)
        if response._error:
            return "❌" + str(response._error)
        return response.text
    except Exception as e:
        return "❌ Exception: " + str(e)               
