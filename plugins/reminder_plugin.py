from psp import Plugin
from datetime import datetime, timedelta
import sqlite3

class ReminderPlugin(Plugin):
    """Plugin for setting reminders on todos"""

    def after_add(self, todo_id, description):
        # Example: Set a reminder for 24 hours from now
        reminder_time = datetime.now() + timedelta(days=1)
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        try:
            c.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    todo_id INTEGER PRIMARY KEY,
                    reminder_time TIMESTAMP,
                    FOREIGN KEY (todo_id) REFERENCES todos (id)
                )
            ''')
            c.execute('INSERT INTO reminders (todo_id, reminder_time) VALUES (?, ?)',
                      (todo_id, reminder_time))
            conn.commit()
            print(f'Reminder set for todo {todo_id} at {reminder_time}')
        except sqlite3.Error as e:
            print(f'Error setting reminder: {e}')
        finally:
            conn.close()