# Open Guild Discord Bot

A powerful Discord bot integrating Gemini AI and OpenAI Assistant for community support, news sharing, and engagement.

## Table of Contents

- [Open Guild Discord Bot](#open-guild-discord-bot)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Codebase Structure](#codebase-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [AI Features](#ai-features)
  - [Contributing](#contributing)
  - [License](#license)

## Description

This Discord bot is built using Python and integrates AI capabilities from Google's Gemini API. It also supports OpenAI Assistant as an alternative AI backend. The bot is designed to provide community support, share news, and enhance engagement within Discord communities, with specific optimizations for blockchain/Polkadot-related discussions.

## Features

- [x] **Community Question Support**
  - [x] Provide accurate and prompt answers to technical and non-technical questions related to:
    - [x] Polkadot's architecture, parachains, XCM, staking, and governance
    - [x] General blockchain concepts, use cases, and emerging trends
  - [x] Assist developers with queries about Polkadot development tools, APIs, and SDKs

- [x] **News Sharing**
  - [x] Aggregate and share the latest Polkadot ecosystem updates
  - [x] Notify the community about important events (runtime upgrades, governance proposals, parachain launches)
  - [x] Highlight key milestones and success stories within the Polkadot ecosystem

- [x] **Community Engagement**
  - [x] Respond to frequently asked questions (FAQs)
  - [x] Guide members to appropriate resources or documentation
  - [x] Promote healthy discussions and foster collaboration among members

- [x] **Advanced Capabilities**
  - [x] PDF content analysis and summarization
  - [x] YouTube video summarization
  - [x] Blog updates tracking
  - [x] Repository monitoring
  - [x] FAQ database maintenance and updates

## Codebase Structure

- **`src/`**: Core logic of the bot
  - **`bot/`**: Fundamental logic for AI interaction and chatbot responses
    - Message processing
    - AI response formatting
    - Documentation handling
  - **`urls/`**: Contains URLs for Blogs, FAQs, and Repositories
  - **`main.py`**: Application entry point

- **`crawl.py`**: Web crawler for FAQ database population
- **`Dockerfile`**: Container configuration for Docker deployment
- **`start.py`**: Deployment script for Railway and local testing

## Prerequisites

- Python 3.8+
- Discord Bot Token
- Google AI API Key (for Gemini)
- OpenAI API Key (optional, for Assistant backend)
- GitHub Token (for repository tracking)

## Installation

1. **Clone the repository**

```bash
git clone git@github.com:Hpgbao2204/builder-support-agent.git
cd builder-support-agent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
GOOGLE_AI_KEY=your_google_ai_key
DISCORD_BOT_TOKEN=your_discord_bot_token
MAX_HISTORY=10  # Number of messages to store in conversation history
GITHUB=your_github_token
# Optional: OPENAI_API_KEY=your_openai_api_key
```

## Usage

**Start the bot**

```bash
python start.py
```

**Docker deployment**

```bash
docker build -t gemini-discord-bot .
docker run -d --env-file .env gemini-discord-bot
```

**Railway deployment**

Configure your Railway project to use the repository and set the environment variables.

## AI Features

The bot's AI capabilities follow a structured process:

1. **Query Processing**
   - Captures user messages in Discord
   - Analyzes intent and context using NLP

2. **Information Retrieval & Response Generation**
   - Checks FAQ database and documentation first
   - Generates AI-driven responses using Gemini or OpenAI
   - Fetches external data via APIs and web scraping when needed
   - Provides optimized answers with contextual awareness
   - Analysis of PDFs and YouTube content

3. **Continuous Learning**
   - Maintains conversation context
   - Logs interactions for performance improvement
   - Updates knowledge bases from configured sources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Insert your license information here]