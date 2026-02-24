# Storage layer for checkbox bot
from typing import Dict, List, Optional

class TodoItem:
    def __init__(self, item_id: str, text: str):
        self.id = item_id
        self.text = text
        self.completed = False

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed
        }


class Storage:
    def __init__(self):
        self.user_todos: Dict[int, List[TodoItem]] = {}
        self.next_id: Dict[int, int] = {}

    def get_or_create_user(self, user_id: int) -> List[TodoItem]:
        if user_id not in self.user_todos:
            self.user_todos[user_id] = []
            self.next_id[user_id] = 1
        return self.user_todos[user_id]

    def add_todo(self, user_id: int, text: str) -> TodoItem:
        todos = self.get_or_create_user(user_id)
        item_id = str(self.next_id[user_id])
        self.next_id[user_id] += 1
        todo = TodoItem(item_id, text)
        todos.append(todo)
        return todo

    def get_todos(self, user_id: int) -> List[TodoItem]:
        return self.get_or_create_user(user_id)

    def get_todo(self, user_id: int, item_id: str) -> Optional[TodoItem]:
        todos = self.get_or_create_user(user_id)
        for todo in todos:
            if todo.id == item_id:
                return todo
        return None

    def toggle_todo(self, user_id: int, item_id: str) -> Optional[TodoItem]:
        todo = self.get_todo(user_id, item_id)
        if todo:
            todo.completed = not todo.completed
        return todo

    def delete_todo(self, user_id: int, item_id: str) -> bool:
        todos = self.get_or_create_user(user_id)
        for i, todo in enumerate(todos):
            if todo.id == item_id:
                todos.pop(i)
                return True
        return False

    def clear_todos(self, user_id: int) -> None:
        if user_id in self.user_todos:
            self.user_todos[user_id] = []

    def get_stats(self, user_id: int) -> Dict[str, int]:
        todos = self.get_or_create_user(user_id)
        total = len(todos)
        completed = sum(1 for todo in todos if todo.completed)
        return {'total': total, 'completed': completed, 'remaining': total - completed}
