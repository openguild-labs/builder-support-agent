# Gemini Discord Bot

## Description

This project is built using Python as the primary language and integrates AI APIs from Gemini. If supported, OpenAI Assistant can also be used as an alternative AI backend.

### Requirements

- Docker
- ```pip install -r requirements.txt```

### Installation

Clone the repository:
  
    ```bash
    git clone https://github.com/yourusername/gemini-bot.git
    cd gemini-bot
    ```

Set up environment variables (you can use a ```.env``` file) 
  ```
  echo "GOOGLE_AI_KEY=<your_google_ai_key>" >> .env
  echo "MAX_HISTORY=<number_of_messages_to_store>" >> .env
  echo "GITHUB=<your_github_token>" >> .env
  echo "DISCORD_BOT_TOKEN=<your_discord_bot_token>" >> .env 
  ```

## Features

- Connects with Gemini AI for intelligent chatbot interactions.
- Stores user chat history based on `MAX_HISTORY` settings.
- Uses GitHub token to track commits.
- Interacts with Discord servers via a bot.