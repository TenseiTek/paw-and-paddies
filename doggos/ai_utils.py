import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("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")

def generate_dog_bio(name, breed, traits):
    # Ensure traits is a list
    if isinstance(traits, str):
        traits = [t.strip() for t in traits.split(',')]

    prompt = f"Write a playful bio for a dog named {name}, a {breed} who is {', '.join(traits)}."

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": prompt
    }

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai-community/gpt2",  # You can swap this model
            headers=headers,
            json=payload
        )
        result = response.json()

        # Handle response format
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"].strip()
        else:
            return generate_fallback_bio(name, breed, traits)

    except Exception as e:
        return f"🐾 Oops! Couldn't fetch a bio: {str(e)}"

def generate_fallback_bio(name, breed, traits):
    if isinstance(traits, str):
        traits = [t.strip() for t in traits.split(',')]

    return f"{name} is a lovable {breed} who’s always {', '.join(traits)} — ready to steal hearts and treats!"