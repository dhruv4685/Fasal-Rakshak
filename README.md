# 🌱 Fasal Rakshak (Agentic AI Farming Advisor)

**Fasal Rakshak** is an AI-powered agricultural advisor designed to assist Indian farmers. It leverages Agentic AI to provide real-time weather updates and expert farming advice using a Retrieval-Augmented Generation (RAG) system.

## 🚀 Features

* **Multi-Interface Access:** Available via a web interface (Streamlit) and a mobile-friendly Telegram Bot.
* **Agentic Intelligence:** The AI intelligently decides when to use tools (like fetching weather) versus general conversation.
* **Real-Time Weather:** Integrated with OpenWeatherMap API to provide live temperature and condition updates for specific cities.
* **Expert Knowledge Base (RAG):** Uses a vector database (ChromaDB) to search through agricultural PDFs for accurate, context-aware advice.
* **Robust Fallback System:** Prioritizes **Google Gemini (2.5-flash)**, but automatically switches to **HuggingFace** or **OpenAI** if the primary model fails.
* **Vernacular Support:** Designed to respond in the user's input language (Hindi/English/etc.).

## 🛠️ Tech Stack

* **Core Logic:** Python, LangChain (Agents & Tools)
* **LLMs:** Google Gemini (Primary), Flan-T5 / GPT-3.5 (Fallback)
* **Vector Database:** ChromaDB
* **Interfaces:** Streamlit (Web), Python-Telegram-Bot (Messaging)
* **APIs:** OpenWeatherMap, Google GenAI

## 📂 Project Structure

* `agent.py`: The brain of the application. Handles model selection and fallback logic.
* `tools.py`: Contains the "hands" of the AI—Weather API calls and PDF retrieval logic.
* `app.py`: The Streamlit web application with dynamic animations.
* `telegram_bot.py`: The asynchronous Telegram bot server.
* `documents/`: Directory for storing agricultural PDFs for the knowledge base.

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/fasal-rakshak.git](https://github.com/yourusername/fasal-rakshak.git)
    cd fasal-rakshak
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    OPENWEATHERMAP_API_KEY=your_weather_api_key
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    HUGGINGFACEHUB_API_TOKEN=your_hf_token
    OPENAI_API_KEY=your_openai_key (optional, for fallback)
    ```

4.  **Run the Web App**
    ```bash
    streamlit run app.py
    ```

5.  **Run the Telegram Bot**
    ```bash
    python telegram_bot.py
    ```

## 👨‍💻 Creator

**Dhruv Kimothi**
* Contact: dhruvkim2005@gmail.com


