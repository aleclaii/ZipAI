from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

#Initialize FastAPI Server: uvicorn app:app --reload

app = FastAPI()
client = OpenAI(api_key="sk-proj-XgsBdcXW871PG9nq3XvUT3BlbkFJtDV6fJsIt9AXDt0baCQI")

#CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://hngpbonhjphcpmnenffbjfgdnakolnfm"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post('/summarize')
async def summarize(request: Request):
    data = await request.json()
    url = data['url']
    
    # WebScrape Script
    content = save_paragraphs_from_url(url)
    
    # Call GPT API
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
        "role": "user",
        "content": f"Summarize the following text: {content}"

        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    summary = response.choices[0].message.content.strip()

    return {'summary': summary}

def save_paragraphs_from_url(url):
    response = requests.get(url)
    articletext = ""
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')

    for p in paragraphs:
        articletext += p.get_text() + "\n"

    return articletext
