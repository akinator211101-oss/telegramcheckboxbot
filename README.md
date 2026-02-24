# Telegram Checkbox Bot

A feature-rich Telegram bot for managing todo lists and checklists with an intuitive command interface.

## Features

- ✅ **Create tasks** - Add new tasks with `/new <task description>`
- 📋 **List tasks** - View all your tasks with completion status
- ✔️ **Mark complete** - Toggle task completion with `/done <task_id>`
- 🗑️ **Delete tasks** - Remove individual tasks with `/delete <task_id>`
- 🧹 **Clear all** - Remove all tasks at once with `/clear`
- 📊 **Statistics** - View task stats with `/stats`

## Installation

### Prerequisites
- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd telegramcheckboxbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your bot token:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

4. Run the bot:
```bash
python bot.py
```

## Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | `/start` | Welcome message and help |
| `/new` | `/new <task>` | Add a new task |
| `/list` | `/list` | Show all tasks |
| `/done` | `/done <id>` | Mark task as complete/incomplete |
| `/delete` | `/delete <id>` | Delete a task |
| `/clear` | `/clear` | Delete all tasks |
| `/stats` | `/stats` | Show task statistics |
| `/help` | `/help` | Show help message |

## Project Structure

```
telegramcheckboxbot/
├── bot.py           # Main bot application
├── handlers.py      # Command handlers
├── storage.py       # Data storage layer
├── requirements.txt # Dependencies
├── tests/
│   ├── test_storage.py    # Storage layer tests
│   ├── test_handlers.py   # Handler tests
│   └── __init__.py
└── README.md
```

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Architecture

- **Storage**: In-memory storage with per-user todo lists
- **Handlers**: Async command handlers for Telegram operations
- **Bot**: Main application using python-telegram-bot library

## License

MIT