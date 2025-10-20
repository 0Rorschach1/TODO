from typing import Union

from models import Project, Task
from service import TodoService

class CLI:
    def __init__(self, service: TodoService):
        self.service = service

    def _print_project(self, project: Project) -> None:
        print(f"ID: {project.id}")
        print(f"Name: {project.name}")
        print(f"Description: {project.description}")
        print("---")

    def _print_task(self, task: Task) -> None:
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Status: {task.status.value}")
        print(f"Deadline: {task.deadline if task.deadline else 'None'}")
        print("---")

    def run(self) -> None:
        while True:
            print("\nTo Do List Menu:")
            print("1. Create Project")
            print("2. List All Projects")
            print("3. Edit Project")
            print("4. Delete Project")
            print("5. Add Task to Project")
            print("6. List Tasks in Project")
            print("7. Change Task Status")
            print("8. Edit Task")
            print("9. Delete Task")
            print("0. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                print("Exiting...")
                break
            elif choice == "1":
                name = input("Enter project name: ").strip()
                description = input("Enter project description: ").strip()
                result = self.service.create_project(name, description)
                if isinstance(result, Project):
                    print("Project created successfully.")
                    self._print_project(result)
                else:
                    print(f"Error: {result}")
            elif choice == "2":
                projects = self.service.get_all_projects()
                if not projects:
                    print("No projects exist.")
                else:
                    print("All Projects:")
                    for project in projects:
                        self._print_project(project)
            elif choice == "3":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    new_name = input("Enter new name (leave blank to keep current): ").strip() or None
                    new_desc = input("Enter new description (leave blank to keep current): ").strip() or None
                    result = self.service.edit_project(project_id, new_name, new_desc)
                    if isinstance(result, Project):
                        print("Project edited successfully.")
                        self._print_project(result)
                    else:
                        print(f"Error: {result}")
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "4":
                try:
                    project_id = int(input("Enter project ID to delete: ").strip())
                    result = self.service.delete_project(project_id)
                    print(result)
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "5":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    title = input("Enter task title: ").strip()
                    description = input("Enter task description: ").strip()
                    status_str = input("Enter status (todo/doing/done, default: todo): ").strip() or "todo"
                    deadline_str = input("Enter deadline (YYYY-MM-DD, optional): ").strip() or None
                    result = self.service.add_task(project_id, title, description, status_str, deadline_str)
                    if isinstance(result, Task):
                        print("Task added successfully.")
                        self._print_task(result)
                    else:
                        print(f"Error: {result}")
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "6":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    result = self.service.get_tasks_in_project(project_id)
                    if isinstance(result, str):
                        print(result)
                    else:
                        print("Tasks in Project:")
                        for task in result:
                            self._print_task(task)
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "7":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    task_id = int(input("Enter task ID: ").strip())
                    new_status = input("Enter new status (todo/doing/done): ").strip()
                    result = self.service.change_task_status(project_id, task_id, new_status)
                    if isinstance(result, Task):
                        print("Task status changed successfully.")
                        self._print_task(result)
                    else:
                        print(f"Error: {result}")
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "8":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    task_id = int(input("Enter task ID: ").strip())
                    new_title = input("Enter new title (leave blank to keep current): ").strip() or None
                    new_desc = input("Enter new description (leave blank to keep current): ").strip() or None
                    new_deadline = input("Enter new deadline (YYYY-MM-DD, leave blank to keep, empty to remove): ").strip() or None
                    new_status = input("Enter new status (todo/doing/done, leave blank to keep): ").strip() or None
                    result = self.service.edit_task(project_id, task_id, new_title, new_desc, new_deadline, new_status)
                    if isinstance(result, Task):
                        print("Task edited successfully.")
                        self._print_task(result)
                    else:
                        print(f"Error: {result}")
                except ValueError:
                    print("Error: Invalid input.")
            elif choice == "9":
                try:
                    project_id = int(input("Enter project ID: ").strip())
                    task_id = int(input("Enter task ID to delete: ").strip())
                    result = self.service.delete_task(project_id, task_id)
                    print(result)
                except ValueError:
                    print("Error: Invalid input.")
            else:
                print("Invalid choice. Please try again.")

