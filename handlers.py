from telegram import Update
from telegram.ext import ContextTypes
from storage import Storage

storage = Storage()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "I'm your checkbox bot. Here are my commands:\n\n"
        "/new <task> - Add a new task\n"
        "/list - Show all tasks\n"
        "/done <id> - Mark task as done\n"
        "/delete <id> - Delete a task\n"
        "/clear - Clear all tasks\n"
        "/help - Show this help message\n"
        "/stats - Show task statistics"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)

async def new_todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /new <task description>")
        return
    
    text = ' '.join(context.args)
    todo = storage.add_todo(user_id, text)
    await update.message.reply_text(f"✅ Added task #{todo.id}: {text}")

async def list_todos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    todos = storage.get_todos(user_id)
    
    if not todos:
        await update.message.reply_text("📝 Your list is empty. Add tasks with /new")
        return
    
    message = "📋 Your tasks:\n\n"
    for todo in todos:
        status = "✅" if todo.completed else "☐"
        message += f"{status} #{todo.id} {todo.text}\n"
    
    await update.message.reply_text(message)

async def toggle_todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /done <task id>")
        return
    
    item_id = context.args[0]
    todo = storage.toggle_todo(user_id, item_id)
    
    if not todo:
        await update.message.reply_text(f"❌ Task #{item_id} not found")
        return
    
    status = "completed" if todo.completed else "reopened"
    await update.message.reply_text(f"✓ Task #{item_id} {status}")

async def delete_todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /delete <task id>")
        return
    
    item_id = context.args[0]
    success = storage.delete_todo(user_id, item_id)
    
    if not success:
        await update.message.reply_text(f"❌ Task #{item_id} not found")
        return
    
    await update.message.reply_text(f"🗑️ Task #{item_id} deleted")

async def clear_todos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    storage.clear_todos(user_id)
    await update.message.reply_text("🧹 All tasks cleared")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    stats_data = storage.get_stats(user_id)
    
    message = (
        f"📊 Your statistics:\n"
        f"Total tasks: {stats_data['total']}\n"
        f"✅ Completed: {stats_data['completed']}\n"
        f"⏳ Remaining: {stats_data['remaining']}"
    )
    await update.message.reply_text(message)
