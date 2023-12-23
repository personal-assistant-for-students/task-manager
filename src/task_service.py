from datetime import datetime, timedelta

from task_model import Task, AdditionalStatus


class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title, content, deadline, user_id):
        new_task = Task(title, content, deadline)
        self.repository.add_task(new_task, user_id)
        return new_task

    def update_task(self, task_id, status, user_id):
        self.repository.update_task(task_id, status, user_id)
        return self.repository.get_task_by_id(task_id, user_id)

    def delete_task(self, task_id, user_id):
        if self.repository.delete_task(task_id, user_id):
            return {"message": f"Task with id {task_id} successfully deleted."}
        else:
            return {"message": f"Task with id {task_id} not found."}

    def get_all_tasks(self, user_id):
        return self.repository.get_all_tasks(user_id)

    def update_additional_statuses(self, user_id):
        all_tasks = self.repository.get_all_tasks(user_id)

        current_datetime = datetime.now()

        for task_id, task_data in all_tasks.items():
            deadline_str = task_data.get('deadline')
            if deadline_str:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                delta = deadline - current_datetime

                if delta < timedelta(days=0):
                    new_additional_status = AdditionalStatus.BURNED.value
                elif delta <= timedelta(days=0):
                    new_additional_status = AdditionalStatus.HELL.value
                elif delta <= timedelta(days=3):
                    new_additional_status = AdditionalStatus.HOT.value
                elif delta <= timedelta(days=8):
                    new_additional_status = AdditionalStatus.WARM.value
                else:
                    new_additional_status = AdditionalStatus.COLD.value

                task_data['additional_status'] = new_additional_status

        self.repository.update_all_tasks(all_tasks, user_id)

    def get_task_by_id(self, task_id, user_id):
        return self.repository.get_task_by_id(task_id, user_id)
