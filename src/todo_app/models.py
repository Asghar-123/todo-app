class Todo:
    def __init__(self, id: int, description: str, is_completed: bool = False):
        if not isinstance(id, int) or id < 0:
            raise ValueError("Todo ID must be a non-negative integer.")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Todo description cannot be empty.")
        if not isinstance(is_completed, bool):
            raise ValueError("Todo is_completed status must be a boolean.")

        self.id = id
        self.description = description.strip()
        self.is_completed = is_completed

    def __repr__(self):
        return f"Todo(id={self.id}, description='{self.description}', is_completed={self.is_completed})"

    def __eq__(self, other):
        if not isinstance(other, Todo):
            return NotImplemented
        return self.id == other.id and self.description == other.description and self.is_completed == other.is_completed
