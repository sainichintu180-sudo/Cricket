from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os
import asyncio

# Environment se token lena (Render me use hota hai)
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("CRICKET_API_KEY")  # cricketdata.org se lo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏏 Welcome! Type /score to get live cricket scores.")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
        response = requests.get(url).json()

        matches = response.get("data", [])
        if not matches:
            await update.message.reply_text("❌ Koi live match nahi mil raha abhi.")
            return

        message = "🏏 *Live Cricket Scores:*\n\n"
        for match in matches[:5]:
            team1 = match["teams"][0]
            team2 = match["teams"][1]
            status = match.get("status", "N/A")
            score_info = ""

            if match.get("score"):
                for s in match["score"]:
                    score_info += f"➡️ {s['inning']}: {s['r']} runs / {s['w']} wickets ({s['o']} overs)\n"

            message += f"*{team1} vs {team2}*\n{score_info}📊 {status}\n\n"

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))

    print("✅ Bot is running on Render...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
