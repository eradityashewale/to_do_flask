import unittest
from app import app, todos_collection
from flask import json
from controllers.to_do.token import API_KEY

class TodoApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.api_key = API_KEY

    def tearDown(self):
        # Clean up the todos collection after each test
        todos_collection.delete_many({})

    # Helper function to add the API key
    def get_headers(self):
        return {'X-API-KEY': self.api_key}
    
    def test_create_todo(self):
        new_todo = {
            'title': 'Test Todo',
            'description': 'Test description'
        }
        response = self.app.post('/todo', data=json.dumps(new_todo), content_type='application/json', headers=self.get_headers())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Todo created', response.json['message'])

    def test_get_all_todos(self):
        # Create a test todo
        todos_collection.insert_one({
            'title': 'Test Todo 1',
            'description': 'Test description 1',
            'status': 'pending',
            'created_at': '2024-09-21T08:45:39.627+00:00',
            'updated_at': '2024-09-21T08:45:39.627+00:00'
        })

        response = self.app.get('/todos', headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json['todos']) > 0)

    def test_get_single_todo(self):
        # Create a test todo
        todo_id = todos_collection.insert_one({
            'title': 'Test Todo 2',
            'description': 'Test description 2',
            'status': 'pending',
            'created_at': '2024-09-21T08:45:39.627+00:00',
            'updated_at': '2024-09-21T08:45:39.627+00:00'
        }).inserted_id

        response = self.app.get(f'/todo/{str(todo_id)}', headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Todo 2', response.json['title'])

    def test_update_todo(self):
        # Create a test todo
        todo_id = todos_collection.insert_one({
            'title': 'Test Todo 3',
            'description': 'Test description 3',
            'status': 'pending',
            'created_at': '2024-09-21T08:45:39.627+00:00',
            'updated_at': '2024-09-21T08:45:39.627+00:00'
        }).inserted_id

        updated_todo = {
            'title': 'Updated Todo Title',
            'description': 'Updated description',
            'status': 'in_progress'
        }

        response = self.app.put(f'/todo/{str(todo_id)}', data=json.dumps(updated_todo), content_type='application/json', headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Todo updated', response.json['message'])

    def test_delete_todo(self):
        # Create a test todo
        todo_id = todos_collection.insert_one({
            'title': 'Test Todo 4',
            'description': 'Test description 4',
            'status': 'pending',
            'created_at': '2024-09-21T08:45:39.627+00:00',
            'updated_at': '2024-09-21T08:45:39.627+00:00'
        }).inserted_id

        response = self.app.delete(f'/todo/{str(todo_id)}', headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Todo deleted', response.json['message'])

if __name__ == '__main__':
    unittest.main()
