import unittest
import os
from src.task_repository import TaskRepository
from src.task_model import Task


class TestTaskRepository(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_db.csv"
        self.repository = TaskRepository(self.test_file_path)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_add_task(self):
        task = Task("Test Task", "Test Content", "2023-12-31")
        self.repository.add_task(task)
        added_task = self.repository.get_task_by_id(str(task.id))
        self.assertEqual(added_task.title, "Test Task")

    def test_update_task(self):
        task = Task("Test Task", "Test Content", "2023-12-31")
        self.repository.add_task(task)
        updated_task = self.repository.update_task(str(task.id), title="Updated Task")
        self.assertEqual(updated_task.title, "Updated Task")

    def test_delete_task(self):
        task = Task("Test Task", "Test Content", "2023-12-31")
        self.repository.add_task(task)
        self.assertTrue(self.repository.delete_task(str(task.id)))

    def test_update_all_tasks(self):
        task1 = Task("Task 1", "Content 1", "2023-12-31")
        task2 = Task("Task 2", "Content 2", "2023-12-31")
        self.repository.add_task(task1)
        self.repository.add_task(task2)

        tasks_data = {
            str(task1.id): task1.to_dict(),
            str(task2.id): task2.to_dict(),
        }

        self.repository.update_all_tasks(tasks_data)

        updated_task1 = self.repository.get_task_by_id(str(task1.id))
        updated_task2 = self.repository.get_task_by_id(str(task2.id))

        self.assertEqual(updated_task1['title'], task1.title)
        self.assertEqual(updated_task2['title'], task2.title)


if __name__ == '__main__':
    unittest.main()
