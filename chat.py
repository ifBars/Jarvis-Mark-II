import os
import json
import google.generativeai as genai
from config import API_KEY, LANGUAGE
from command_modules_init import all_commands_str, additional_info_str

with open(os.path.join("locales", "system_instructions.json"), "r", encoding="utf8") as f:
    instructions = json.load(f)
    
lang_instructions = instructions.get(LANGUAGE, instructions["en"])

system_instruction = (
    f"{lang_instructions['base']}\n"
    f"{all_commands_str}{additional_info_str}\n"
    f"{lang_instructions['ending']}"
)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
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

