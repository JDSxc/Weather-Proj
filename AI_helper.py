import requests
from secrets_helper import get_api_key
#from groq import Groq

GROQ_API_KEY = get_api_key("GROQ_API_KEY")

def groqValidateInput(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    model="llama3-70b-8192"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model,
        "messages": [
            {
                "role": "system", 
                "content": "Given a short location input like 'hcmc vn' or 'austin texas us' or 'Los Angeles', "
                "If you are given a city name, within your best knowledge return it with the correct JSON format"
                "If multiple cities match, return your first match"
                "Return ONLY valid JSON with ONLY the following keys: city, state, country. "
                "Use the full name for city, state, and country. "
                "You MUST validate that the city actually exists in that state and country. "
                "If it's invalid or does not exist in the given country/state, reply ONLY with: "
                "{\"Error\": \"invalid input\"}"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }
    response = requests.post(url, headers=headers, json=body)
    content= response.json()['choices'][0]['message']['content']
    return content
#print(groqValidateInput("San Antonio"))