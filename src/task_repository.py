class TaskRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = {}

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_task_by_id(self, task_id):
        return self.tasks.get(task_id, None)

    def add_task(self, task):
        self.tasks[str(task.id)] = task

    def update_task(self, task_id, **kwargs):
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)

        self.tasks[task_id] = task

        return task

    def delete_task(self, task_id):
        if task_id in self.tasks.keys():
            del self.tasks[task_id]
            return True  # успешно удалена
        return False  # не найдена

    def update_all_tasks(self, updated_tasks):
        for task_id, updated_data in updated_tasks.items():
            if task_id in self.tasks:
                self.tasks[task_id] = updated_data
        self.save_to_file()

    def save_to_file(self):
        tasks_csv = "\n".join(
            [f"{task_id},{','.join(task_data.values())}" for task_id, task_data in self.tasks.items()])

        with open(self.file_path, 'w') as file:
            file.write(tasks_csv)
