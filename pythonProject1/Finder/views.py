from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from google.adk.planners import PlanReActPlanner
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types, Client
import os
from google.generativeai import configure
from dotenv import load_dotenv
from django.contrib.auth.models import User
from contextlib import aclosing
load_dotenv()
import asyncio
api_key = os.getenv("API_KEY")
# Use api_key as argument when initializing your Google AI client
client = Client(api_key=api_key)
APP_NAME = "basic-agent-no-web"
USER_ID = "user12345"
SESSION_ID = "12345"



def signup_view(request):
    username= request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.create_user(username=username,email=email, password=password)
    user.save()
    login(request,user)
    return render(request, "Finder/signup.html")
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, "Finder/login.html", {"message":"Logged in"})
        else:
            return render(request, "Finder/login.html",{"message":"User not found"})
    return render(request, "Finder/login.html")
def logout_view(request):
    logout(request)
    return render(request, 'Finder/index.html')
async def home(request):
    task_agent1 = Agent(
        name="task_agent",
        model="gemini-2.5-flash",
        instruction="You have to recommend one task to user to do in a current stock market without any personal portfolio and description only 6 to 10 words .remove markdown formats",
        description="Recommending users to do certain tasks for stock markets",
        #tools=""
    )
    task_agent2 = Agent(
        name="task_agent",
        model="gemini-2.5-flash",
        instruction="You have to recommend one task to user to do in a current stock market wihout any personal portfolio and description only 6 to 10 words .remove markdown formats",
        description="Recommending users to do certain tasks for stock markets",
        # tools=""
    )

    session_service1 = InMemorySessionService()
    await session_service1.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner1 = Runner(app_name=APP_NAME, agent=task_agent1, session_service=session_service1)
    content1 = types.Content(role="user", parts=[types.Part(text="Please remove all the markdown formats and get all recomendations")])
    events1 = runner1.run_async(new_message=content1, user_id=USER_ID, session_id=SESSION_ID)
    session_service2 = InMemorySessionService()
    await session_service2.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner2 = Runner(app_name=APP_NAME, agent=task_agent1, session_service=session_service2)
    content2 = types.Content(role="user", parts=[
        types.Part(text="Please remove all the markdown formats and get all recomendations")])
    events2 = runner2.run_async(new_message=content2, user_id=USER_ID, session_id=SESSION_ID)

    async for event1 in events1:
        if event1.is_final_response():
            response1 = event1.content.parts[0].text
            print(response1)
    async for event2 in events2:
        if event2.is_final_response():
            response2 = event2.content.parts[0].text
            print(response2)
    return render(request, "Finder/index.html",{"task1":response1.replace("[","") and response1,"task2":response2})



async def stocks(request):

    stocker = request.POST.get("stock")
    print(stocker)

    stock_agent = Agent(
        name="google_search_agent",
        model="gemini-2.5-flash",
        instruction="You are a stock analyser. Give professional stock advice for everyone for current time and tell if stock should be purchased or not also provided some charts and links for research along with disclaimer. PLease remove all the markdown formats",
        description="Professional search assistant with Google Search capabilities",
        planner=PlanReActPlanner(),
        tools=[google_search]
    )

    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(app_name=APP_NAME, agent=stock_agent, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=stocker+"Please all the markdown formats")])
    events = runner.run_async(new_message=content, user_id=USER_ID, session_id=SESSION_ID)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
    return render(request, 'Finder/index.html',{"response" : final_response})


async def screening(request):
    if request.method == "POST":
        stocks_agent = Agent(
            name="stocks_agent",
            model="gemini-2.5-pro",
            instruction="You have to give all stocks to in a current stock market .remove markdown formats",
            description="Giving running stocks",
            output_key="stocks"
        )
        best = Agent(
            name="best_stocks_agent",
            model="gemini-2.5-pro",
            instruction="You have to 10 best stocks in a current stock market from {stocks} .remove markdown formats",
            description="Giving best stocks out of running stocks",
        )
        coordinator = SequentialAgent(name="Coordinator", sub_agents=[stocks_agent,best])
        initial_input = request.POST.get("criteria-input")
        session_service = InMemorySessionService()
        await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        runner = Runner(app_name=APP_NAME, agent=coordinator, session_service=session_service)
        content = types.Content(role="user", parts=[types.Part(text=initial_input)])
        events = runner.run_async(new_message=content, user_id=USER_ID, session_id=SESSION_ID)
        async for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text

        return render(request, "Finder/screener.html", {"response": final_response})
    return render(request, "Finder/screener.html")

def apps(request):
    return render(request, "Finder/apps.html")