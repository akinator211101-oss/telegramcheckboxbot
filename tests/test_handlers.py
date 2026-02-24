# Test suite for handlers
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, User, Chat, Message
from handlers import storage, new_todo, list_todos, toggle_todo, delete_todo, clear_todos, stats, start, help_command


@pytest.fixture
def mock_update():
    update = AsyncMock(spec=Update)
    update.effective_user = MagicMock()
    update.effective_user.id = 123
    update.effective_user.first_name = "TestUser"
    update.message = AsyncMock()
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    context = MagicMock()
    context.args = []
    return context


@pytest.fixture(autouse=True)
def reset_storage():
    storage.user_todos.clear()
    storage.next_id.clear()
    yield
    storage.user_todos.clear()
    storage.next_id.clear()


class TestStartHandler:
    @pytest.mark.asyncio
    async def test_start(self, mock_update, mock_context):
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Welcome TestUser" in call_args
        assert "/new" in call_args
        assert "/list" in call_args


class TestHelpHandler:
    @pytest.mark.asyncio
    async def test_help(self, mock_update, mock_context):
        await help_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()


class TestNewTodoHandler:
    @pytest.mark.asyncio
    async def test_new_todo_with_text(self, mock_update, mock_context):
        mock_context.args = ["Buy", "groceries"]
        await new_todo(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Added task #1" in call_args
        assert "Buy groceries" in call_args

    @pytest.mark.asyncio
    async def test_new_todo_without_text(self, mock_update, mock_context):
        mock_context.args = []
        await new_todo(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Usage: /new" in call_args


class TestListHandler:
    @pytest.mark.asyncio
    async def test_list_empty(self, mock_update, mock_context):
        await list_todos(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "empty" in call_args.lower()

    @pytest.mark.asyncio
    async def test_list_with_todos(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        await list_todos(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Task 1" in call_args
        assert "Task 2" in call_args
        assert "#1" in call_args
        assert "#2" in call_args

    @pytest.mark.asyncio
    async def test_list_shows_completion_status(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        storage.toggle_todo(123, "1")
        await list_todos(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "✅" in call_args


class TestToggleTodoHandler:
    @pytest.mark.asyncio
    async def test_toggle_existing_todo(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        mock_context.args = ["1"]
        await toggle_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "completed" in call_args

    @pytest.mark.asyncio
    async def test_toggle_nonexistent_todo(self, mock_update, mock_context):
        mock_context.args = ["999"]
        await toggle_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "not found" in call_args

    @pytest.mark.asyncio
    async def test_toggle_without_id(self, mock_update, mock_context):
        mock_context.args = []
        await toggle_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Usage: /done" in call_args


class TestDeleteTodoHandler:
    @pytest.mark.asyncio
    async def test_delete_existing_todo(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        mock_context.args = ["1"]
        await delete_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "deleted" in call_args.lower()

    @pytest.mark.asyncio
    async def test_delete_nonexistent_todo(self, mock_update, mock_context):
        mock_context.args = ["999"]
        await delete_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "not found" in call_args

    @pytest.mark.asyncio
    async def test_delete_without_id(self, mock_update, mock_context):
        mock_context.args = []
        await delete_todo(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Usage: /delete" in call_args


class TestClearTodosHandler:
    @pytest.mark.asyncio
    async def test_clear(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        await clear_todos(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "cleared" in call_args.lower()
        assert len(storage.get_todos(123)) == 0


class TestStatsHandler:
    @pytest.mark.asyncio
    async def test_stats_empty(self, mock_update, mock_context):
        await stats(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Total tasks: 0" in call_args

    @pytest.mark.asyncio
    async def test_stats_with_items(self, mock_update, mock_context):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        storage.toggle_todo(123, "1")
        await stats(mock_update, mock_context)
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Total tasks: 2" in call_args
        assert "Completed: 1" in call_args
        assert "Remaining: 1" in call_args
