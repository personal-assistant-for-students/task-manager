import uuid
from datetime import datetime, timedelta
from enum import Enum


class TaskStatus(Enum):
    TO_DO = "Сделать"
    IN_PROGRESS = "Делаю"
    DONE = "Выполнено"


class AdditionalStatus(Enum):
    COLD = "Холодный"
    WARM = "Теплый"
    HOT = "Горит"
    HELL = "Адище"
    BURNED = "Сгорел"


class Task:
    def __init__(self, title, content, deadline):
        self.id = uuid.uuid4()
        self._title = title
        self._content = content
        self._deadline = deadline
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.status = TaskStatus.TO_DO
        self.additional_status = self.calculate_additional_status()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.updated_at = datetime.now()

    @title.getter
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self.updated_at = datetime.now()

    @content.getter
    def content(self):
        return self._content

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value
        self.updated_at = datetime.now()
        self.additional_status = self.calculate_additional_status()

    @deadline.getter
    def deadline(self):
        return self._deadline

    def calculate_additional_status(self):
        now = datetime.now()
        deadline_datetime = datetime.strptime(self.deadline, '%Y-%m-%d')
        delta = deadline_datetime - now

        if delta <= timedelta(days=0):
            return AdditionalStatus.BURNED
        elif delta <= timedelta(days=1):
            return AdditionalStatus.HELL
        elif delta <= timedelta(days=5):
            return AdditionalStatus.HOT
        elif delta <= timedelta(days=10):
            return AdditionalStatus.WARM
        else:
            return AdditionalStatus.COLD

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self._title,
            "content": self._content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deadline": self._deadline,
            "status": self.status.value,
            "additional_status": self.additional_status.value
        }
