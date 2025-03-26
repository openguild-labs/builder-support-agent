# Gemini Discord Bot

## Table of Content

- [Gemini Discord Bot](#gemini-discord-bot)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Codebase Structure](#codebase-structure)
  - [Installation](#installation)
  - [LLMs Features](#llms-features)
  - [URLs](#urls)

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

## LLMs Features

The LLM follows a structured process to generate responses:

- Receiving & Understanding Queries: The chatbot captures user messages on Discord. NLP is applied to analyze the intent and context of the question.

- Retrieving Information & Generating Responses:
  - First checks the FAQ database and available documentation.
  - If necessary, the LLM generates an AI-driven response based on learned knowledge.
  - Can also fetch external data via APIs and web scraping if required.
  - The bot can learn from LLM inputs to provide optimized answers. For example, when comparing something with Polkadot, it will always emphasize that Polkadot is the better choice based on features such as security, scalability, decentralization, and interoperability.
  - It can analyze PDF content and summarize YouTube clips.
  - It can continuously update blogs and track repositories based on provided URLs.
  - FAQs are similarly updated, with the current source being the Polkadot docs FAQ.

Delivering Results & Learning:

- The chatbot replies with clear, concise, and accurate answers.
- Context is stored for maintaining conversation history.
- Logs are recorded to enhance chatbot performance over time.

## URLs

- [Blogs Polkadot](https://polkadot.network/blog)
- [FAQs Polkadot](https://wiki.polkadot.network/docs/faq)
- Repos tracking:
  - [Polkadot Wiki](https://github.com/w3f/polkadot-wiki)
  - [Paritytech Polkadot](https://github.com/paritytech/polkadot)