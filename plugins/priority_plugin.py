from psp import Plugin
import sqlite3

class PriorityPlugin(Plugin):
    """Plugin for managing todo priorities"""

    def before_add(self, description):
        # Add priority table if it doesn't exist
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        try:
            c.execute('''
                CREATE TABLE IF NOT EXISTS priorities (
                    todo_id INTEGER PRIMARY KEY,
                    priority INTEGER DEFAULT 0,
                    FOREIGN KEY (todo_id) REFERENCES todos (id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f'Error initializing priority table: {e}')
        finally:
            conn.close()

    def after_add(self, todo_id, description):
        # Set default priority
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO priorities (todo_id, priority) VALUES (?, ?)',
                      (todo_id, 1))
            conn.commit()
            print(f'Set default priority for todo {todo_id}')
        except sqlite3.Error as e:
            print(f'Error setting priority: {e}')
        finally:
            conn.close()