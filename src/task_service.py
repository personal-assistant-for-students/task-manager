from datetime import datetime, timedelta

from task_model import Task, AdditionalStatus


class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title, content, deadline):
        new_task = Task(title, content, deadline)
        self.repository.add_task(new_task)
        return new_task

    def update_task(self, task_id, status):
        self.repository.update_task(task_id, status)
        return self.repository.get_task_by_id(task_id)

    def delete_task(self, task_id):
        if self.repository.delete_task(task_id):
            return {"message": f"Task with id {task_id} successfully deleted."}
        else:
            return {"message": f"Task with id {task_id} not found."}

    def get_all_tasks(self):
        return self.repository.get_all_tasks()

    def update_additional_statuses(self):
        all_tasks = self.repository.get_all_tasks()

        current_datetime = datetime.now()

        for task_id, task_data in all_tasks.items():
            deadline_str = task_data.get('deadline')
            if deadline_str:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                delta = deadline - current_datetime

                if delta <= timedelta(days=0):
                    new_additional_status = AdditionalStatus.BURNED.value
                elif delta <= timedelta(days=1):
                    new_additional_status = AdditionalStatus.HELL.value
                elif delta <= timedelta(days=5):
                    new_additional_status = AdditionalStatus.HOT.value
                elif delta <= timedelta(days=10):
                    new_additional_status = AdditionalStatus.WARM.value
                else:
                    new_additional_status = AdditionalStatus.COLD.value

                task_data['additional_status'] = new_additional_status

        self.repository.update_all_tasks(all_tasks)

    def get_task_by_id(self, task_id):
        return self.repository.get_task_by_id(task_id)
