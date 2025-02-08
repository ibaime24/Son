import base64
from openai import OpenAI
import os

# Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

client = OpenAI()


# Helper function to encode image

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Main function to process image and question

def process_image_and_question(image_path: str, question: str) -> str:
    base64_image = encode_image(image_path)
    
    system_context = """You are Son, a concise yet informative vision assistant for the visually impaired. Start descriptions with 'I see'"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_context
            },
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content 