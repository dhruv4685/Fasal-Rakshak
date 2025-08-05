# app.py

import streamlit as st
from dotenv import load_dotenv
import requests

# --- UI Enhancement Imports ---
from streamlit_lottie import st_lottie

# --- LangChain Imports ---
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Import our custom tools ---
from tools import get_weather, get_agri_advice, create_knowledge_base_retriever
from agent import load_agent_executor
load_dotenv()

# --- Lottie Animation URLs ---
LOTTIE_URL_SUN = "https://lottie.host/dd59b58a-38a3-4888-8461-125b74c2e646/zPYdYENs3S.json"
LOTTIE_URL_CLOUDS = "https://lottie.host/89163259-b996-4819-8d6a-c2540cb628b0/5v2sI52OCa.json"
LOTTIE_URL_RAIN = "https://lottie.host/36905470-b1ac-46a2-9721-399719325764/3s1iS23a4o.json"
# --- NEW, WORKING URL FOR THINKING ANIMATION ---
LOTTIE_URL_THINKING = "https://lottie.host/5f3d8234-93b5-4a6c-a812-58f7f2d408e0/VdY22a5i6M.json"


def load_lottieurl(url: str):
    """Fetches a Lottie animation from a URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Agent and Tools Loading (Cached) ---
@st.cache_resource
def load_agent_executor():
    """Loads and caches the LangChain agent and its components."""
    print("--- Loading Agent Executor for the first time ---")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, convert_system_message_to_human=True)
    
    retriever = create_knowledge_base_retriever()
    
    tools = [
        Tool(
            name="WeatherForecast",
            func=get_weather,
            description="Use this tool to get the current weather for a specific city. Input should be a city name."
        ),
        Tool(
            name="AgriculturalKnowledgeBase",
            func=lambda query: get_agri_advice(query, retriever),
            description="Use this tool to get advice on farming practices, crop management, drought, pests, etc., based on expert documents."
        )
    ]
    
    prompt_template_str = """
    You are a helpful AI farm advisor named 'Fasal Rakshak'. Your goal is to help farmers in the Jodhpur, Rajasthan region.
    You are conversational and empathetic. You MUST strictly respond in the exact same language as the user's input.

    You have access to the following tools: {tools}

    To use a tool, use the following format:
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    Thought: Do I need to use a tool? No
    Final Answer: [your response to the user here, in the user's exact language]

    Begin!
    New input: {input}
    {agent_scratchpad}
    """
    prompt = PromptTemplate.from_template(template=prompt_template_str)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

agent_executor = load_agent_executor()

# --- UI Styling ---
st.set_page_config(page_title="Fasal Rakshak", page_icon="🌱", layout="centered")

image_url = "https://i.postimg.cc/cJ9bMbwJ/background-jpg.jpg" 

css = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url({image_url});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* All other CSS rules */
    body, p, li, .st-emotion-cache-1c7y2kd {{ color: #FFFFFF !important; font-weight: 500 !important; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(15, 23, 42, 0.8); }}
    div[data-testid="chat-message-container"]:has(div[data-testid="chat-avatar-user"]) {{ background-color: #0891B2; }}
    div[data-testid="chat-message-container"]:has(div[data-testid="chat-avatar-assistant"]) {{ background-color: #334155; }}
    a:link, a:visited {{ color: #38BDF8; }}
    a:hover, a:active {{ color: #7DD3FC; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.title("🌱 Fasal Rakshak")
    st.subheader("Your AI Farming Assistant")
    
    current_weather = get_weather("Jodhpur").lower()
    weather_lottie_url = LOTTIE_URL_CLOUDS # Default
    if "rain" in current_weather or "drizzle" in current_weather:
        weather_lottie_url = LOTTIE_URL_RAIN
    elif "sun" in current_weather or "clear" in current_weather:
        weather_lottie_url = LOTTIE_URL_SUN
    
    lottie_weather = load_lottieurl(weather_lottie_url)
    if lottie_weather:
        st_lottie(lottie_weather, height=150, key="weather_animation")

    st.markdown("---")
    st.markdown("Built for the Indian Agri Ecosystem.")
    st.markdown("Powered by Google Gemini & LangChain.")

# --- Main Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask Fasal Rakshak a question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- UPDATED and more robust assistant response block ---
    with st.chat_message("assistant"):
        response_generated = False
        with st.spinner(""):
            thinking_animation = load_lottieurl(LOTTIE_URL_THINKING)
            
            if thinking_animation:
                st_lottie(thinking_animation, height=100, key="thinking_animation")
            
            response = agent_executor.invoke({"input": user_input})
            response_generated = True

        if response_generated:
            st.markdown(response['output'])
            st.balloons()
            st.session_state.messages.append({"role": "assistant", "content": response['output']})