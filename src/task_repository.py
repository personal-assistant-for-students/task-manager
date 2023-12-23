from task_model import TaskStatus


class TaskRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = {}  # Внешний словарь: {user_id: внутренний словарь}

    def add_task(self, task, user_id):
        if user_id not in self.tasks:
            self.tasks[user_id] = {}  # Если пользователь еще не существует, создаем для него внутренний словарь
        self.tasks[user_id][str(task.id)] = task

    def get_all_tasks(self, user_id):
        # Фильтрация задач, чтобы вернуть только те, у которых статус не DONE
        if user_id not in self.tasks:
            self.tasks[user_id] = {}
        return [task for task in self.tasks[user_id].values() if task.status != TaskStatus.DONE]

    def get_task_by_id(self, task_id, user_id):
        tasks = (self.tasks.get(user_id, None))
        return tasks.get(task_id, None)

    def update_task(self, task_id, status, user_id):
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Проверяем, существует ли такой статус в TaskStatus
        valid_status = next((s for s in TaskStatus if s.value == status), None)
        if valid_status:
            # Устанавливаем статус, если он найден
            task.status = valid_status
        else:
            # Возвращаем None, если статус не найден
            return None

        # Сохраняем обновленную задачу
        self.tasks[user_id][task_id] = task
        return task

    def delete_task(self, task_id, user_id):
        if task_id in self.tasks[user_id].keys():
            del self.tasks[user_id][task_id]
            return True  # успешно удалена
        return False  # не найдена

    def update_all_tasks(self, updated_tasks, user_id):
        for task_id, updated_data in updated_tasks.items():
            if task_id in self.tasks[user_id]:
                self.tasks[user_id][task_id] = updated_data
        self.save_to_file(user_id)

    def save_to_file(self, user_id):  # TODO для user id
        tasks_csv = "\n".join(
            [f"{task_id},{','.join(task_data.values())}" for task_id, task_data in self.tasks.items()])

        with open(self.file_path + "_" + user_id + ".csv", 'w') as file:
            file.write(tasks_csv)
