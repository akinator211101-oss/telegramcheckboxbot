# Test suite for storage module
import pytest
from storage import Storage, TodoItem


class TestTodoItem:
    def test_create_todo_item(self):
        todo = TodoItem("1", "Buy groceries")
        assert todo.id == "1"
        assert todo.text == "Buy groceries"
        assert todo.completed is False

    def test_todo_item_to_dict(self):
        todo = TodoItem("1", "Buy groceries")
        data = todo.to_dict()
        assert data == {
            'id': '1',
            'text': 'Buy groceries',
            'completed': False
        }


class TestStorage:
    @pytest.fixture
    def storage(self):
        return Storage()

    def test_get_or_create_user(self, storage):
        todos = storage.get_or_create_user(123)
        assert todos == []
        assert 123 in storage.user_todos

    def test_add_todo(self, storage):
        todo = storage.add_todo(123, "First task")
        assert todo.id == "1"
        assert todo.text == "First task"
        assert todo.completed is False

    def test_add_multiple_todos(self, storage):
        todo1 = storage.add_todo(123, "Task 1")
        todo2 = storage.add_todo(123, "Task 2")
        assert todo1.id == "1"
        assert todo2.id == "2"

    def test_get_todos(self, storage):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        todos = storage.get_todos(123)
        assert len(todos) == 2
        assert todos[0].text == "Task 1"
        assert todos[1].text == "Task 2"

    def test_get_todo(self, storage):
        storage.add_todo(123, "Task 1")
        todo = storage.get_todo(123, "1")
        assert todo is not None
        assert todo.text == "Task 1"

    def test_get_todo_not_found(self, storage):
        todo = storage.get_todo(123, "999")
        assert todo is None

    def test_toggle_todo(self, storage):
        storage.add_todo(123, "Task 1")
        todo = storage.toggle_todo(123, "1")
        assert todo.completed is True
        
        todo = storage.toggle_todo(123, "1")
        assert todo.completed is False

    def test_toggle_nonexistent_todo(self, storage):
        todo = storage.toggle_todo(123, "999")
        assert todo is None

    def test_delete_todo(self, storage):
        storage.add_todo(123, "Task 1")
        success = storage.delete_todo(123, "1")
        assert success is True
        assert len(storage.get_todos(123)) == 0

    def test_delete_nonexistent_todo(self, storage):
        success = storage.delete_todo(123, "999")
        assert success is False

    def test_clear_todos(self, storage):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        storage.clear_todos(123)
        assert len(storage.get_todos(123)) == 0

    def test_get_stats_empty(self, storage):
        stats = storage.get_stats(123)
        assert stats == {'total': 0, 'completed': 0, 'remaining': 0}

    def test_get_stats_with_items(self, storage):
        storage.add_todo(123, "Task 1")
        storage.add_todo(123, "Task 2")
        storage.toggle_todo(123, "1")
        stats = storage.get_stats(123)
        assert stats == {'total': 2, 'completed': 1, 'remaining': 1}

    def test_isolated_user_data(self, storage):
        storage.add_todo(123, "User 1 Task")
        storage.add_todo(456, "User 2 Task")
        
        todos_123 = storage.get_todos(123)
        todos_456 = storage.get_todos(456)
        
        assert len(todos_123) == 1
        assert len(todos_456) == 1
        assert todos_123[0].text == "User 1 Task"
        assert todos_456[0].text == "User 2 Task"
