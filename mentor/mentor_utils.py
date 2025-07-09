# mentor_utils.py

from openai import OpenAI
import os
from decouple import config
client = OpenAI(api_key=config("OPENAI_API_KEY"))

def process_mentor_chat(user_input: str) -> str:
    """
    Processes the user input using OpenAI GPT and returns a structured response.

    Args:
        user_input (str): The business idea input from the user.

    Returns:
        str: Formatted multilingual assistant response.
    """
    system_message = """
You are a multilingual business assistant chatbot. For every user message:

1. Detect the language.
2. Respond ONLY in that same language.
3. Extract and return the following fields:
   - BUSINESS_TYPE
   - CAPITAL
   - LOCATION
   - TARGET
   - SECTOR
   - TIMELINE
   - EXPERIENCE

4. Provide:
   - A feasibility score out of 10 with reasons.
   - Government scheme matching (Indian context): scheme name, eligibility, required papers, loan amount, and interest rate explanation.
   - A business plan (5-step).
   - Personalized advice, voice-friendly.

Use bullet points and structured formatting in the same language as the input.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()
