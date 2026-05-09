from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io

# load the environment
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=gemini_api_key)

# note generator
def note_generator(images):
    prompt = """Summarize the picture in note format at max 100 words
    make sure to add necessary markdown to differentiate different section"""
    
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images, prompt],
    )
    return response.text


def create_audio(text):
    speech = gTTS(text, lang= 'en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer


def create_quiz(images, difficulty):
    prompt = f"Create 3 quizzes based on the images and the difficulty level of {difficulty}. Make sure output the result in markdown"
    
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images, prompt],
    )
    return response.text