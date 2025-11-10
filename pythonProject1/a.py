from django.shortcuts import render

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types, Client
import os
from google.generativeai import configure
from dotenv import load_dotenv
load_dotenv()
import asyncio
api_key = os.getenv("API_KEY")
# Use api_key as argument when initializing your Google AI client
client = Client(api_key=api_key)
APP_NAME = "basic-agent-no-web"
USER_ID = "user12345"
SESSION_ID = "12345"

def home(request):
    if request.method == "POST":
        stock = request.POST.get("stock")
        root_agent = Agent(
            name="google_search_agent",
            model="gemini-2.5-flash",
            instruction="You are a stock analyser. Give professional stock advice for everyone for current time and tell if stock should be purchased or not also provided some charts and links for research along with disclaimer",
            description="Professional search assistant with Google Search capabilities",
            tools=[google_search]
        )
        session_service = InMemorySessionService()
        session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)
        content = types.Content(role="user", parts=[types.Part(text=stock)])
        events = runner.run_async(new_message=content, user_id=USER_ID, session_id=SESSION_ID)

        for event in events:
            if event.is_final_response():
                global final_response
                final_response = event.content.parts[0].text

            return render(request, 'Analyse/index.html',{"response" : final_response})
    return render(request, 'Analyse/index.html')

