from typing import List, Optional

from models import Project, Task

class InMemoryRepository:
    def __init__(self):
        self.projects: List[Project] = []
        self.project_id_counter: int = 1

    def add_project(self, project: Project) -> None:
        self.projects.append(project)
        # Removed: self.project_id_counter += 1 to require manual ID management

    def get_all_projects(self) -> List[Project]:
        return self.projects

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        for project in self.projects:
            if project.id == project_id:
                return project
        return None

    def update_project(self, updated_project: Project) -> None:
        for i, project in enumerate(self.projects):
            if project.id == updated_project.id:
                self.projects[i] = updated_project
                break

    def delete_project(self, project_id: int) -> bool:
        for i, project in enumerate(self.projects):
            if project.id == project_id:
                del self.projects[i]
                return True
        return False

    def add_task_to_project(self, project: Project, task: Task) -> None:
        project.tasks.append(task)
        # Removed: project.task_id_counter += 1 to require manual ID management

    def get_task_by_id(self, project: Project, task_id: int) -> Optional[Task]:
        for task in project.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, project: Project, updated_task: Task) -> None:
        for i, task in enumerate(project.tasks):
            if task.id == updated_task.id:
                project.tasks[i] = updated_task
                break

    def delete_task(self, project: Project, task_id: int) -> bool:
        for i, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[i]
                return True
        return False
