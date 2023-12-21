import unittest
import json
from src.task_app import app
from src.task_model import Task, TaskStatus
from src.task_service import TaskService
from src.task_repository import TaskRepository


class TestTaskController(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.test_file_path = "test_db.csv"
        self.repository = TaskRepository(self.test_file_path)
        self.task_service = TaskService(self.repository)

    def tearDown(self):
        pass

    def test_create_task(self):
        task_data = {
            "title": "Test Task",
            "content": "Test Content",
            "deadline": "2023-12-31"
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertEqual(data["title"], task_data["title"])
        self.assertEqual(data["content"], task_data["content"])
        self.assertEqual(data["deadline"], task_data["deadline"])
        self.assertEqual(data["status"], TaskStatus.TO_DO.value)

    def test_update_task(self):
        task = Task("Task 1", "Content 1", "2023-12-31")
        self.repository.add_task(task)

        updated_data = {
            "title": "Updated Task",
            "content": "Updated Content",
            "deadline": "2024-01-01"
        }
        response = self.app.put(f'/tasks/{str(task.id)}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, dict)
        self.assertEqual(data["title"], updated_data["title"])
        self.assertEqual(data["content"], updated_data["content"])
        self.assertEqual(data["deadline"], updated_data["deadline"])

    def test_delete_task(self):
        task = Task("Task 1", "Content 1", "2023-12-31")
        self.repository.add_task(task)

        response = self.app.delete(f'/tasks/{str(task.id)}')
        self.assertEqual(response.status_code, 200)
