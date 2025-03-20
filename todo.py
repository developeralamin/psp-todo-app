import os
import sqlite3
import click
from psp import Plugin, PluginManager
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore

# Initialize colorama for colored output
init(autoreset=True)

# Initialize Plugin Manager
plugin_manager = PluginManager('todo_plugins')

# Database setup
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Plugin interface
class TodoPlugin(Plugin):
    def before_add(self, description):
        pass

    def after_add(self, todo_id, description):
        pass

    def before_complete(self, todo_id):
        pass

    def after_complete(self, todo_id):
        pass

@click.group()
def cli():
    """Todo application with plugin support"""
    init_db()

@cli.command()
@click.argument('description')
def add(description):
    """Add a new todo"""
    # Execute before_add plugins
    for plugin in plugin_manager.get_plugins():
        plugin.before_add(description)

    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (description) VALUES (?)', (description,))
    todo_id = c.lastrowid
    conn.commit()
    conn.close()

    # Execute after_add plugins
    for plugin in plugin_manager.get_plugins():
        plugin.after_add(todo_id, description)

    click.echo(Fore.GREEN + f'Added todo: {description}')

@cli.command()
def list():
    """List all todos"""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('SELECT id, description, completed, created_at, completed_at FROM todos')
    todos = c.fetchall()
    conn.close()

    if not todos:
        click.echo(Fore.YELLOW + 'No todos found')
        return

    headers = ['ID', 'Description', 'Status', 'Created', 'Completed']
    table_data = []
    for todo in todos:
        status = Fore.GREEN + '✓' if todo[2] else Fore.RED + '✗'
        created = datetime.strptime(todo[3], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
        completed = datetime.strptime(todo[4], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M') if todo[4] else '-'
        table_data.append([todo[0], todo[1], status, created, completed])

    click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))

@cli.command()
@click.argument('todo_id', type=int)
def complete(todo_id):
    """Mark a todo as complete"""
    # Execute before_complete plugins
    for plugin in plugin_manager.get_plugins():
        plugin.before_complete(todo_id)

    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?', (todo_id,))
    if c.rowcount == 0:
        click.echo(Fore.RED + f'No todo found with ID {todo_id}')
    else:
        conn.commit()
        click.echo(Fore.GREEN + f'Marked todo {todo_id} as complete')
        # Execute after_complete plugins
        for plugin in plugin_manager.get_plugins():
            plugin.after_complete(todo_id)
    conn.close()

@cli.command()
@click.argument('todo_id', type=int)
def delete(todo_id):
    """Delete a todo"""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    if c.rowcount == 0:
        click.echo(Fore.RED + f'No todo found with ID {todo_id}')
    else:
        conn.commit()
        click.echo(Fore.GREEN + f'Deleted todo {todo_id}')
    conn.close()

@cli.command()
@click.argument('todo_id', type=int)
@click.argument('description')
def update(todo_id, description):
    """Update a todo's description"""
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('UPDATE todos SET description = ? WHERE id = ?', (description, todo_id))
    if c.rowcount == 0:
        click.echo(Fore.RED + f'No todo found with ID {todo_id}')
    else:
        conn.commit()
        click.echo(Fore.GREEN + f'Updated todo {todo_id}')
    conn.close()

if __name__ == '__main__':
    cli()