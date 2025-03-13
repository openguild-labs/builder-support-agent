# Gemini Discord Bot

## Table of Content

- [Gemini Discord Bot](#gemini-discord-bot)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Codebase Structure](#codebase-structure)
  - [Installation](#installation)
  - [Features](#features)


## Description

This project is built using Python as the primary language and integrates AI APIs from Gemini. If supported, OpenAI Assistant can also be used as an alternative AI backend.

## Codebase Structure
- `src/` directory: Contains the core logic of the bot, structured into three mains:
  - `bot/` directory: Contains the fundamental logic for interacting with Gemini AI and processing chatbot responses. This includes the Docs, message processing, and AI response formatting.
  - `urls/` directory: Contains URLs for Blogs, FAQs, Repos
  - `main.py`: Run application
- `crawl.py`: Crawl URLs to get database for FAQs
- `Dockerfile`: Deploy bot by Docker
- `start.py`: Deploy bot on Railway and Local for testing

## Installation

Clone the repository:
  
    ```bash
    git clone git@github.com:Hpgbao2204/builder-support-agent.git
    cd builder-support-agent
    ```
Start project: 
  ```bash
  pip install -r requirement.txt
  # SET ENV KEY 
  python3 start.py
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
- Custom prompt
- Custom URLs for tracking commits, faqs, blogs
  