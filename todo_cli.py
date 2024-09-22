import argparse
import requests
from flask import request

API_URL = "http://localhost:5000"  # The base URL for your API

# Function to get all todos
def get_todos(page=1, limit=10):
    response = requests.get(f"{API_URL}/todos", params={'page': page, 'limit': limit})
    print(response.json())

# Function to get a specific todo by ID
def get_todo(todo_id):
    response = request.get(f"{API_URL}/todo/{todo_id}")
    print(response.json())

# Function to create a new todo
def create_todo(title, description, status):
    data = {
        'title': title,
        'description': description,
        'status': status,
    }
    response = requests.post(f"{API_URL}/todos", json=data)
    print(response.json())

# Function to update an existing todo by ID
def update_todo(todo_id, title=None, description=None, status=None):
    data = {}
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    if status:
        data['status'] = status

    response = requests.put(f"{API_URL}/todo/{todo_id}", json=data)
    print(response.json())

# Function to delete a todo by ID
def delete_todo(todo_id):
    response = requests.delete(f"{API_URL}/todo/{todo_id}")
    print(response.json())

# Main function for the CLI
def main():
    parser = argparse.ArgumentParser(description="Todo CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for GET todos
    subparsers.add_parser('get', help='Get all todos')

    # Subparser for GET a specific todo
    get_parser = subparsers.add_parser('get_todo', help='Get a specific todo')
    get_parser.add_argument('id', type=str, help='ID of the todo')

    # Subparser for creating a todo
    create_parser = subparsers.add_parser('create', help='Create a new todo')
    create_parser.add_argument('title', type=str, help='Title of the todo')
    create_parser.add_argument('description', type=str, help='Description of the todo')
    create_parser.add_argument('status', type=str, choices=['pending', 'in_progress', 'completed'], help='Status of the todo')

    # Subparser for updating a todo
    update_parser = subparsers.add_parser('update', help='Update an existing todo')
    update_parser.add_argument('id', type=str, help='ID of the todo')
    update_parser.add_argument('--title', type=str, help='New title of the todo')
    update_parser.add_argument('--description', type=str, help='New description of the todo')
    update_parser.add_argument('--status', type=str, choices=['pending', 'in_progress', 'completed'], help='New status of the todo')

    # Subparser for deleting a todo
    delete_parser = subparsers.add_parser('delete', help='Delete a todo')
    delete_parser.add_argument('id', type=str, help='ID of the todo')

    args = parser.parse_args()

    if args.command == 'get':
        get_todos()  # Get all todos
    elif args.command == 'get_todo':
        get_todo(args.id)  # Get a specific todo by ID
    elif args.command == 'create':
        create_todo(args.title, args.description, args.status)  # Create a new todo
    elif args.command == 'update':
        update_todo(args.id, args.title, args.description, args.status)  # Update a todo by ID
    elif args.command == 'delete':
        delete_todo(args.id)  # Delete a todo by ID

if __name__ == '__main__':
    main()
