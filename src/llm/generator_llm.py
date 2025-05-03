from langchain_ibm import WatsonxLLM
from src.llm.prompt_template import video_creating_prompt, create_caption, create_hashtags
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY", None)
PROJECT_ID = os.getenv("PROJECT_ID", None)
MODEL_URL = os.getenv("WML_URL", None)

def setup_watsonx_llm_video():

    model_id_answer_gen = "meta-llama/llama-3-405b-instruct"
    #model_id_answer_gen = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"


    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 200,
        "repetition_penalty": 1}

    watsonx_llm = WatsonxLLM(
        model_id=model_id_answer_gen,
        url=MODEL_URL,
        apikey=API_KEY,
        project_id=PROJECT_ID,
        params=parameters,
    )
    return watsonx_llm

def setup_watsonx_llm():
    model_id_answer_gen = "meta-llama/llama-3-405b-instruct"

    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 500,
        "repetition_penalty": 1}

    watsonx_llm = WatsonxLLM(
        model_id=model_id_answer_gen,
        url=MODEL_URL,
        apikey=API_KEY,
        project_id=PROJECT_ID,
        params=parameters,
    )
    return watsonx_llm


llm = setup_watsonx_llm_video()

brand_name = "Starbucks"
product = "Beverages"
target = "Gen Z"
tone = "funny"

trend_description= "Italian Brainrot is a series of surrealist Internet memes that emerged in early 2025, characterized by absurd photos of AI-generated creatures with Italian names. The memes often feature characters with absurd and ironic names, such as Tung Tung Tung Tung Tung Tung Tung Saer, Capuccino Asashino, and Boneca Amvalabu. The memes have gained popularity on social media platforms such as TikTok and Reddit, with many users creating and sharing their own Italian Brainrot characters. The phenomenon has also inspired a theater play, a coloring book, and a musical."


prompt_hashtag_creation = create_caption()

prompt_hashtags = prompt_hashtag_creation.format(
        brand_name=brand_name,
        product=product,
        tone=tone)


r = llm.invoke(prompt_hashtags)

print(r)