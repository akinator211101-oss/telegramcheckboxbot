import os
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, new_todo, list_todos, toggle_todo, delete_todo, clear_todos, stats

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("new", new_todo))
    app.add_handler(CommandHandler("list", list_todos))
    app.add_handler(CommandHandler("done", toggle_todo))
    app.add_handler(CommandHandler("delete", delete_todo))
    app.add_handler(CommandHandler("clear", clear_todos))
    app.add_handler(CommandHandler("stats", stats))
    
    app.run_polling()

if __name__ == '__main__':
    main()
