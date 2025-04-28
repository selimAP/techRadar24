# Twitter Tech News Bot

An automated Twitter bot that fetches and posts the latest tech news at regular intervals.

## Features

- Fetches the latest tech news using NewsAPI
- Automatically generates relevant hashtags
- Tweets news articles every 3 hours
- Lightweight and easy to configure

## Requirements

- Python 3.8+
- Twitter API credentials
- NewsAPI key

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:selimAP/techRadar24.git
cd techRadar24
```
### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file with your API keys

Create a file named `.env` in the project root directory and add the following content:

```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET_KEY=your_api_secret_key
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
NEWS_API_KEY=your_newsapi_key
```

## Usage

To start the bot, run:

```bash
python bot.py
```



