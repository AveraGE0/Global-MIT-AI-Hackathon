import os

from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

from src.llm.prompt_template import prediction_forecast

load_dotenv()

API_KEY = os.getenv("API_KEY", None)
PROJECT_ID = os.getenv("PROJECT_ID", None)
MODEL_URL = os.getenv("WML_URL", None)


def setup_watsonx_llm_video():

    model_id_answer_gen = "meta-llama/llama-3-405b-instruct"
    # model_id_answer_gen = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"

    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 200,
        "repetition_penalty": 1,
    }

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
        "repetition_penalty": 1,
    }

    watsonx_llm = WatsonxLLM(
        model_id=model_id_answer_gen,
        url=MODEL_URL,
        apikey=API_KEY,
        project_id=PROJECT_ID,
        params=parameters,
    )
    return watsonx_llm
