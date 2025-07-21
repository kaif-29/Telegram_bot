import os
import logging
import asyncio
import nest_asyncio
import random
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Load environment (if needed)
load_dotenv()
TOKEN = "8005399318:AAFmHmgWVSq9XlyX5PxkizgVrYkxhC6phpE"
WEATHER_API_KEY = "5ffc5230a5b400b87c5df60d9995ddaa"

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Quotes list
QUOTES = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "You miss 100% of the shots you don't take. – Wayne Gretzky",
    "Whether you think you can or you think you can’t, you’re right. – Henry Ford",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "Be yourself; everyone else is already taken. — Oscar Wilde",
    # ... (rest of the quotes can continue here)
]

# Affirmations list
AFFIRMATIONS = [
    "🌟 You are capable of amazing things.",
    "💪 You are stronger than you think.",
    "🔥 Every day is a new beginning.",
    "🎯 You can do hard things.",
    "🌈 Believe in yourself and magic will happen.",
    "✨ You are enough, just as you are.",
    "🧘 Breathe. Everything is going to be okay.",
    "🌞 Every day is a fresh start.",
    "🦋 You are growing and evolving.",
    "💖 You are deeply loved and valued.",
    "🌠 Your dreams are valid and achievable.",
    "🎈 Let go of fear, embrace joy.",
    "🌻 You bring light to those around you.",
    "🚀 You’re on the right path. Keep going!",
    "🍀 Something wonderful is about to happen.",
    "🏔 You can overcome any challenge.",
    "💡 Your ideas matter.",
    "🧩 You are an important piece of the universe.",
    "🌊 You have the power to change your story.",
    "🎨 You are creative and full of potential.",
    "📚 You are always learning and improving.",
    "🔑 You already have what it takes.",
    "🌺 You are a beautiful person inside and out.",
    "🎧 Peace begins with you.",
    "⚡ You are strong, focused, and determined.",
    "🌼 You radiate confidence and courage.",
    "🛤 Trust the timing of your life.",
    "🏅 You are making progress every day.",
    "🪴 You are growing at your own pace.",
    "💎 You are unique and that’s your power.",
    "🧠 You are smart, capable, and resourceful.",
    "💬 Your voice deserves to be heard.",
    "🕊 You deserve inner peace and happiness.",
    "💫 You attract positivity and abundance.",
    "🎯 You are aligned with your purpose.",
    "🌍 The world is better because you're in it.",
    "🌙 You deserve rest, not guilt."
]

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your bot.\nTry /help to see all commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available commands:\n"
        "/start - Start the bot\n"
        "/help - Help info\n"
        "/quote - Get a random quote\n"
        "/weather <city> - Weather in a city\n"
        "/define <word> - Word meaning\n"
        "/roll - Roll a dice 🎲\n"
        "/toss - Toss a coin 🪙\n"
        "/affirm - Get a daily affirmation"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Quote of the moment:\n\n" + random.choice(QUOTES))

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /weather <city>")
        return

    city = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        res = requests.get(url).json()
        if res.get("cod") != 200:
            await update.message.reply_text("❌ City not found.")
            return
        msg = (
            f"🌦 Weather in {city.title()}:\n"
            f"Temp: {res['main']['temp']}°C\n"
            f"Condition: {res['weather'][0]['description'].title()}\n"
            f"Humidity: {res['main']['humidity']}%\n"
            f"Wind: {res['wind']['speed']} m/s"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Could not fetch weather.")

async def define(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /define <word>")
        return

    word = context.args[0]
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        res = requests.get(url).json()
        if isinstance(res, list):
            definition = res[0]['meanings'][0]['definitions'][0]['definition']
            await update.message.reply_text(f"📚 *{word}* means:\n{definition}", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Word not found.")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Could not fetch definition.")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎲 You rolled a {random.randint(1, 6)}!")

async def toss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🪙 It's {random.choice(['Heads', 'Tails'])}!")

async def affirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(AFFIRMATIONS))

# Main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("define", define))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("toss", toss))
    app.add_handler(CommandHandler("affirm", affirm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("✅ Bot is polling…")
    await app.run_polling()

# Run
nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())
