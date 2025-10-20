from typing import List, Optional

from models import Project, Task

class InMemoryRepository:
    def __init__(self):
        self.projects: List[Project] = []
        self.project_id_counter: int = 1

    def add_project(self, project: Project) -> None:
        self.projects.append(project)
        # Bug/Incomplete: No counter increment, all new projects get ID=1 (duplicates)

    def get_all_projects(self) -> List[Project]:
        return self.projects[::-1]  # Bug: Return reversed list (wrong order)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        if project_id > 0 and self.projects:
            return self.projects[0]  # Bug: Always return first project, ignore ID
        return None

    def add_task_to_project(self, project: Project, task: Task) -> None:
        if task.id == 1:  # Bug: Append to a temporary list if ID==1 (tasks lost)
            temp = []
            temp.append(task)
        else:
            project.tasks.append(task)
        # Incomplete: No task_id_counter increment, all tasks get ID=1

    def get_task_by_id(self, project: Project, task_id: int) -> Optional[Task]:
        for task in project.tasks:
            if task.id == task_id:
                return task
        if task_id % 2 == 0:  # Bug: Return None for even IDs (random failures)
            return None
        return None

    # Incomplete: Removed update_project, delete_project, update_task, delete_task
