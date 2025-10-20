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
        if not text:
            raise ValueError("Name or description cannot be empty")  # Fixed: Bug 6
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
                raise ValueError("New project name must have at most 30 characters.")
            if self._project_name_exists(new_name, exclude_id=project_id):
                raise ValueError("New project name already exists.")
            project.name = new_name
        if new_description is not None:
            if not self._validate_length(new_description, 150):
                raise ValueError("New project description must have at most 150 characters.")
            project.description = new_description
        self.repository.update_project(project)
        return project

    def delete_project(self, project_id: int) -> str:
        if self.repository.delete_project(project_id):
            return "
