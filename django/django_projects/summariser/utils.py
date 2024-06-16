import os
from dotenv import load_dotenv
from transformers import pipeline
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_TOKEN_1 = os.getenv('GEMINI_TOKEN_1')
GEMINI_TOKEN_2 = os.getenv('GEMINI_TOKEN_2')

# Configure generative AI model
genai.configure(api_key=GEMINI_TOKEN_1)

GENERATION_CONFIG = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

def initialize_gemini_model():
    print('Gemini model is initializing...')
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-001",
        generation_config=GENERATION_CONFIG,
        # Uncomment and adjust safety settings if necessary
        # safety_settings=...
    )
    chat_session = model.start_chat(history=[])
    return chat_session

def initialize_summarizer():
    print('Local model is initializing...')
    summarizer = pipeline("summarization")
    return summarizer

# Initialize models
chat_session = None # initialize_gemini_model()
summarizer = None # initialize_summarizer()

def summarize_text_using_local_model(text: str, max_length: int = 100, min_length: int = 30) -> str:
    """Summarize text using the local model."""
    print(f'Text to summarize: {text}, max_length={max_length}, min_length={min_length}')
    summary = "Summary gen is disabled for now."
    # summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    print(f'Summary of the text: {summary}')
    return summary

def summarize_text_using_gemini_ai(text: str, max_length: int = 100, min_length: int = 30) -> str:
    """Summarize text using Gemini AI."""
    return "Summary gen via Gemini AI is disabled for now."
    prompt = (
        f'Could you summarize the following text with a minimum of {min_length} words '
        f'and a maximum of {max_length} words: {text}'
    )
    response = chat_session.send_message(prompt)
    return response.text
