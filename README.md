# PSP Todo Application

A simple and extensible Todo application built using Python Simple Plugin System (PSP).

## Features

- Add, remove, and update todos
- List all todos with status and timestamps
- Mark todos as complete/incomplete
- Plugin system for extending functionality
- SQLite database for persistent storage
- Colored output for better visibility

## Installation

1. Clone the repository:
```bash
git clone https://github.com/developeralamin/psp-todo-app.git
cd psp-todo-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application provides the following commands:

- Add a todo:
```bash
python todo.py add "Task description"
```

- List all todos:
```bash
python todo.py list
```

- Mark a todo as complete:
```bash
python todo.py complete <todo_id>
```

- Delete a todo:
```bash
python todo.py delete <todo_id>
```

- Update a todo:
```bash
python todo.py update <todo_id> "New description"
```

## Plugin Development

The application supports plugins through the PSP system. To create a new plugin:

1. Create a new Python file in the `plugins` directory
2. Implement the `TodoPlugin` interface
3. Use the following hooks:
   - `before_add(description)`
   - `after_add(todo_id, description)`
   - `before_complete(todo_id)`
   - `after_complete(todo_id)`

Example plugin template:
```python
from psp import Plugin

class MyPlugin(Plugin):
    def before_add(self, description):
        # Do something before adding a todo
        pass

    def after_add(self, todo_id, description):
        # Do something after adding a todo
        pass

    def before_complete(self, todo_id):
        # Do something before completing a todo
        pass

    def after_complete(self, todo_id):
        # Do something after completing a todo
        pass
```

## License

MIT License