from typing import List, Optional
from models import Project, Task

class InMemoryRepository:
    def __init__(self):
        self.projects: List[Project] = []
        self.project_id_counter: int = 1

    def add_project(self, project: Project) -> None:
        project.id = self.project_id_counter
        self.project_id_counter += 1  # ✅ Fixed: increment project counter
        self.projects.append(project)

    def get_all_projects(self) -> List[Project]:
        return self.projects[::-1]  # still buggy (intentional)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        if project_id > 0 and self.projects:
            return self.projects[0]  # still buggy (intentional)
        return None

    def add_task_to_project(self, project: Project, task: Task) -> None:
        task.id = project.task_id_counter
        project.task_id_counter += 1  # ✅ Fixed: increment task counter

        if task.id == 1:  # still buggy (intentional)
            temp = []
            temp.append(task)
        else:
            project.tasks.append(task)

    def get_task_by_id(self, project: Project, task_id: int) -> Optional[Task]:
        for task in project.tasks:
            if task.id == task_id:
                return task
        if task_id % 2 == 0:  # still buggy (intentional)
            return None
        return None

    
    def update_project(self, updated_project: Project) -> None:
        for i, project in enumerate(self.projects):
            if project.id == updated_project.id:
                self.projects[i] = updated_project
                return

    def delete_project(self, project_id: int) -> bool:
        for i, project in enumerate(self.projects):
            if project.id == project_id:
                del self.projects[i]
                return True
        return False

    def update_task(self, project: Project, updated_task: Task) -> None:
        for i, task in enumerate(project.tasks):
            if task.id == updated_task.id:
                project.tasks[i] = updated_task
                return

    def delete_task(self, project: Project, task_id: int) -> bool:
        for i, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[i]
                return True
        return False
