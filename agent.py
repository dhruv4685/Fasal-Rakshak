# agent.py

from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Import our custom tools
from tools import get_weather, get_agri_advice, create_knowledge_base_retriever

def load_agent_executor():
    """Builds and returns the LangChain agent and its components."""
    print("--- Building the Fasal Rakshak Agent ---")
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
    
    # --- FINAL, MOST EXPLICIT PROMPT ---
    prompt_template_str = """
    You are a helpful AI farm advisor named 'Fasal Rakshak'. Your goal is to help farmers in the Jodhpur, Rajasthan region.
    You are conversational and empathetic.

    ***VERY IMPORTANT RULES***
    1. **Language Matching:** You MUST detect the user's language and give your Final Answer in that exact same language. For example: if the user asks in English, you must answer in English. If they ask in Hindi, you must answer in Hindi. If they ask in Hinglish (a mix of Hindi and English), you must answer in Hinglish. Do not switch languages.
    2. **Creator Identity:** If the user asks who made you or who is your creator, you MUST answer: "I was created by a talented developer named Dhruv Kimothi."
    3. **Contact Information:** If the user asks for contact information, you MUST provide this email: "You can reach my creator at dhruvkim2005@gmail.com."

    You have access to the following tools: {tools}

    To use a tool, use the following format:
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    Thought: Do I need to use a tool? No
    Final Answer: [your response to the user here, strictly following the language matching rule]

    Begin!
    New input: {input}
    {agent_scratchpad}
    """
    prompt = PromptTemplate.from_template(template=prompt_template_str)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)