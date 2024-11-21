# 🎲 S-Casino

## Overview

Welcome to **S-Casino**! This is a fun and interactive bot where you can play simple games like coin flips, dice rolls, and more. The goal is to have fun while demonstrating your skills in Python and creative thinking. The bot stores user data like balance and game history in a local database.

## Getting Started

### Prerequisites

Before running the bot, make sure you have the following:

- Python 3.10+
- Docker (if running in a containerized environment)
- Docker Compose (for managing multi-container Docker applications)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/telegram-bot-game.git
    cd telegram-bot-game
    ```

2. **Install dependencies:**

    If you're using a virtual environment, you can install the required packages with:

    ```bash
    pip install -r requirements.txt
    ```

    Docker Compose will handle the rest of the setup, so you don't need to manually set up anything else for the database or other dependencies.

### Configuration

1. **Set up Telegram bot token:**

    Create a `.env` file in the root directory of the project and add your bot's token:

    ```env
    TELEGRAM_API_TOKEN=your_telegram_bot_token
    TIME_BONUS_AMOUNT=1000
    COIN_FLIP_GIF_URL=https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHEwZHh5ZzFjZzlkZGc1YWR4ZGkycnNoa3J3MmZjb3M3aG9xNzdjciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y4cMaANkENnOxDEPe6/giphy.gif
    DICE_GIT_URL=https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3BrcWd2OWI0djU3bWo2cHhnNjVjbGFscHBoZW8zbGZkb2RwNmh5biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/H8emGexVWRACH5X08H/giphy.gif
    ```

2. **Database Configuration:**

    The bot uses an SQLite database to store user information, including balances and game history. The database will be automatically set up when the bot starts.

### Running the Bot with Docker Compose

To start the bot using Docker Compose, follow these steps:

1. **Build and start the containers:**

    ```bash
    docker-compose up --build
    ```

    This will:

    - Build the Docker image for the bot
    - Start the bot in a container
    - Set up the SQLite database if it doesn't exist

2. **Run the bot in detached mode:**

    If you want to run the bot in the background:

    ```bash
    docker-compose up -d
    ```

3. **Stop the containers:**

    To stop the running containers, use:

    ```bash
    docker-compose down
    ```![img.png](img.png)

If you prefer to run the bot directly without Docker, follow these steps:

1. **Install Python Dependencies:**

    Ensure you have Python 3.8+ installed. Create a virtual environment and install the required dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    pip3 install -r requirements.txt
    ```

2. **Run the Bot:**

    Start the bot with the following command:

    ```bash
    python run.py
    ```

3. **Stop the Bot:**

    Press `Ctrl+C` in the terminal to stop the bot.

---
