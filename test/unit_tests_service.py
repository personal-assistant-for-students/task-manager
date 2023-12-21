import unittest
from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.task_model import Task


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.repository = TaskRepository("test_db.csv")
        self.service = TaskService(self.repository)

    def tearDown(self):
        import os
        if os.path.exists("test_db.csv"):
            os.remove("test_db.csv")

    def test_create_task(self):
        task_data = {
            "title": "Test Task",
            "content": "Test Content",
            "deadline": "2023-12-31"
        }
        task = self.service.create_task(**task_data)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, task_data["title"])
        self.assertEqual(task.content, task_data["content"])
        self.assertEqual(task.deadline, task_data["deadline"])

    def test_update_task(self):
        task = Task("Task 1", "Content 1", "2023-12-31")
        self.repository.add_task(task)

        updated_data = {
            "title": "Updated Task",
            "content": "Updated Content",
            "deadline": "2024-01-01"
        }
        updated_task = self.service.update_task(str(task.id), **updated_data)
        self.assertIsInstance(updated_task, Task)
        self.assertEqual(updated_task.title, updated_data["title"])
        self.assertEqual(updated_task.content, updated_data["content"])
        self.assertEqual(updated_task.deadline, updated_data["deadline"])

    def test_delete_task(self):
        task = Task("Task 1", "Content 1", "2023-12-31")
        self.repository.add_task(task)

        response = self.service.delete_task(str(task.id))
        self.assertTrue(response["message"].startswith("Task with id"))
        self.assertTrue("successfully deleted" in response["message"])

    def test_get_all_tasks(self):
        task1 = Task("Task 1", "Content 1", "2023-12-31")
        task2 = Task("Task 2", "Content 2", "2023-12-31")
        self.repository.add_task(task1)
        self.repository.add_task(task2)

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)


if __name__ == '__main__':
    unittest.main()
