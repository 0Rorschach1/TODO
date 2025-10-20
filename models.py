class Task:
    def __init__(self, id, title, description, status, deadline=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline


class Project:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.tasks = []
        self.task_id_counter = 1
