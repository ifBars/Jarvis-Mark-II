import os
import json
import google.generativeai as genai
from config import API_KEY, LANGUAGE, PERSONALITY, GEMINI_MODEL
from command_modules_init import all_commands_str, additional_info_str
from personality import load_personality
    
personality_instructions = load_personality(PERSONALITY, LANGUAGE)

system_instruction = (
    f"{personality_instructions['base']}\n"
    f"{all_commands_str}{additional_info_str}\n"
    f"{personality_instructions['ending']}"
)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    generation_config=generation_config,
    system_instruction=system_instruction
)

chat_session = model.start_chat()

def send_to_jarvis(message, process_command_func, speak_func):
    """
    Send the user's message to the AI model and process the response.
    The response text is parsed for commands (via process_command_func), then spoken and any sound effects played.
    """
    response = chat_session.send_message(message)
    cleaned_response = process_command_func(response.text)
    print("Jarvis:", response.text)
    speak_func(cleaned_response)

