import os
from flask import Flask
from src.main import run_bot
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Gemini Bot is running!"

# Run Flask on separate thread
def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
