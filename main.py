import os
from dotenv import load_dotenv

from models import Project, Task, Status
from repository import InMemoryRepository
from service import TodoService
from cli import CLI

def main():
    load_dotenv()
    repo = InMemoryRepository()
    service = TodoService(repo)
    cli = CLI(service)
    cli.run()

if __name__ == "__main__":
    main()

