from task_model import TaskStatus


class TaskRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = {}

    def get_all_tasks(self):
        # Фильтрация задач, чтобы вернуть только те, у которых статус не DONE
        return [task for task in self.tasks.values() if task.status != TaskStatus.DONE]

    def get_task_by_id(self, task_id):
        return self.tasks.get(task_id, None)

    def add_task(self, task):
        self.tasks[str(task.id)] = task

    def update_task(self, task_id, status):
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Извлекаем значение статуса из словаря
        status_value = status.get('status')

        # Проверяем, существует ли такой статус в TaskStatus
        valid_status = next((s for s in TaskStatus if s.value == status_value), None)
        if valid_status:
            # Устанавливаем статус, если он найден
            task.status = valid_status
        else:
            # Возвращаем None, если статус не найден
            return None

        # Сохраняем обновленную задачу
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
