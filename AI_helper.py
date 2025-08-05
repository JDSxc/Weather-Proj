import requests
from secrets_helper import get_api_key
from requests.exceptions import Timeout, RequestException
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
                "content": "Given a short location input like 'hcmc vn', 'austin texas us', or 'Los Angeles':\n"
                        "1. Parse the input into three fields: city, state (or province), and country.\n"
                        "2. Normalize each to its full, official English name.\n"
                        "3. Verify that the city exists in the specified state and country.\n"
                        "   If multiple matches exist, choose the first.\n"
                        "   If the city has been renamed or no longer exists, map it to its current name at the same location "
                        "(e.g. 'Constantinople, Byzantine' -> Istanbul, Turkey).\n"
                        "4. PRODUCE ONLY A SINGLE JSON OBJECT with EXACTLY these keys (in this order):\n"
                        "   {\"city\":\"<Full City Name>\",\"state\":\"<Full State/Province Name or empty string>\",\"country\":\"<Full Country Name>\"}\n"
                        "5. Do NOT output any extra text, comments, or whitespace outside the JSON.\n"
                        "6. If validation fails for any reason, output exactly: {\"Error\":\"invalid_input\"}\n"
                        "Ensure your response is always valid JSON so that json.loads(...) never breaks."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    try:
        #raise RequestException("simulated network failure") # simulate groq being unavailable
        response = requests.post(url, headers=headers, json=body)
        content= response.json()['choices'][0]['message']['content']
        return content
    except (RequestException) as e:
        raise

#print(groqValidateInput("San Antonio"))