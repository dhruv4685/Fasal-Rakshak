# telegram_bot.py

# --- NEW: Add these two lines at the very top ---
import nest_asyncio
nest_asyncio.apply()
# ---------------------------------------------

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import the agent loader from our central agent.py file
from agent import load_agent_executor

async def main():
    """Starts the bot."""
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Load the agent
    print("Loading Fasal Rakshak agent...")
    agent_executor = load_agent_executor()
    print("Agent loaded successfully.")

    # Create the Telegram Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handler for when a user first starts a chat
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Namaste! I am Fasal Rakshak. How can I help you with your farm today?")

    # Message handler for all text messages
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        chat_id = update.message.chat_id
        print(f"Received message from {chat_id}: '{user_message}'")
        
        # Let the user know the agent is thinking
        await context.bot.send_chat_action(chat_id=chat_id, action='typing')

        try:
            # Invoke the agent with the user's message
            response = agent_executor.invoke({"input": user_message})
            agent_reply = response['output']
        except Exception as e:
            print(f"Error invoking agent: {e}")
            agent_reply = "I'm sorry, I encountered an error. Please try again."
        
        # Send the agent's reply back to the user
        await update.message.reply_text(agent_reply)

    # Add the handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot is running. Press Ctrl+C to stop.")
    # Start polling for new messages
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())