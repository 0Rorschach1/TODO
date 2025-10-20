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
    deadline = None
    if deadline_str:
        try:
            deadline = date.fromisoformat(deadline_str)  # Fixed: Bug 4
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
                task.deadline = date.fromisoformat(new_deadline_str)  # Fixed: Bug 4
            except ValueError:
                raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
    if new_status_str is not None:
        try:
            task.status = Status(new_status_str)
        except ValueError:
            raise ValueError("Invalid status. Must be 'todo', 'doing', or 'done'.")
    self.repository.update_task(project, task)
    return task
