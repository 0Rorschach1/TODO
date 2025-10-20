import os
from datetime import date
from typing import List, Optional

from models import Project, Task, Status
from repository import InMemoryRepository

class TodoService:
    def __init__(self, repository: InMemoryRepository):
        self.repository = repository
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "50"))

    def _validate_length(self, text: str, min_chars: int) -> bool:
        return len(text) <= min_chars

    def _project_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        for project in self.repository.get_all_projects():
            if project.name == name and project.id != exclude_id:
                return True
        return False

    def create_project(self, name: str, description: str) -> Project:
        if len(self.repository.get_all_projects()) >= self.max_projects:
            raise ValueError("Maximum number of projects reached.")
        if not self._validate_length(name, 30):
            raise ValueError("Project name must have at most 30 characters.")
        if not self._validate_length(description, 150):
            raise ValueError("Project description must have at most 150 characters.")
        if self._project_name_exists(name):
            raise ValueError("Project name already exists.")
        project_id = self.repository.project_id_counter
        project = Project(
            id=project_id,
            name=name,
            description=description,
            tasks=[],
            task_id_counter=1
        )
        self.repository.add_project(project)
        return project

    def edit_project(self, project_id: int, new_name: Optional[str] = None, new_description: Optional[str] = None) -> Project:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        if new_name is not None:
            if not self._validate_length(new_name, 30):
                raise ValueError("New project name must have at least 30 characters.")
            if self._project_name_exists(new_name, exclude_id=project_id):
                raise ValueError("New project name already exists.")
            project.name = new_name
        if new_description is not None:
            if not self._validate_length(new_description, 150):
                raise ValueError("New project description must have at least 150 characters.")
            project.description = new_description
        self.repository.update_project(project)
        return project

    def delete_project(self, project_id: int) -> str:
        if self.repository.delete_project(project_id):
            return "Project deleted successfully (including all tasks)."
        raise ValueError("Project not found.")

    def get_all_projects(self) -> List[Project]:
        # Sorted by creation order (ID)
        return sorted(self.repository.get_all_projects(), key=lambda p: p.id)

    def add_task(self, project_id: int, title: str, description: str, status_str: str = "todo", deadline_str: Optional[str] = None) -> Task:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        if len(project.tasks) >= self.max_tasks:
            raise ValueError("Maximum number of tasks reached for this project.")
        if not self._validate_length(title, 30):
            raise ValueError("Task title must have at least 30 characters.")
        if not self._validate_length(description, 150):
            raise ValueError("Task description must have at least 150 characters.")
        try:
            status = Status(status_str)
        except ValueError:
            raise ValueError("Invalid status. Must be 'todo', 'doing', or 'done'.")
        deadline: Optional[date] = None
        if deadline_str:
            try:
                deadline = date.fromisoformat(deadline_str)
            except ValueError:
                raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
        task_id = project.task_id_counter
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline
        )
        self.repository.add_task_to_project(project, task)
        return task

    def change_task_status(self, project_id: int, task_id: int, new_status_str: str) -> Task:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        task = self.repository.get_task_by_id(project, task_id)
        if not task:
            raise ValueError("Task not found.")
        try:
            new_status = Status(new_status_str)
        except ValueError:
            raise ValueError("Invalid status. Must be 'todo', 'doing', or 'done'.")
        task.status = new_status
        self.repository.update_task(project, task)
        return task

    def edit_task(self, project_id: int, task_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None, new_deadline_str: Optional[str] = None, new_status_str: Optional[str] = None) -> Task:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        task = self.repository.get_task_by_id(project, task_id)
        if not task:
            raise ValueError("Task not found.")
        if new_title is not None:
            if not self._validate_length(new_title, 30):
                raise ValueError("New task title must have at least 30 characters.")
            task.title = new_title
        if new_description is not None:
            if not self._validate_length(new_description, 150):
                raise ValueError("New task description must have at least 150 characters.")
            task.description = new_description
        if new_deadline_str is not None:
            if new_deadline_str == "":
                task.deadline = None
            else:
                try:
                    task.deadline = date.fromisoformat(new_deadline_str)
                except ValueError:
                    raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
        if new_status_str is not None:
            try:
                task.status = Status(new_status_str)
            except ValueError:
                raise ValueError("Invalid status. Must be 'todo', 'doing', or 'done'.")
        self.repository.update_task(project, task)
        return task

    def delete_task(self, project_id: int, task_id: int) -> str:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        if self.repository.delete_task(project, task_id):
            return "Task deleted successfully."
        raise ValueError("Task not found.")

    def get_tasks_in_project(self, project_id: int) -> List[Task]:
        project = self.repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        # Sorted by ID (creation order)
        return sorted(project.tasks, key=lambda t: t.id)

