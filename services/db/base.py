from abc import ABC, abstractmethod
from uuid import UUID
from models import Project


class DBClient(ABC):
    @abstractmethod
    def get_projects(self, page_num: int, page_size: int) -> list[Project]:
        pass
    
    @abstractmethod
    def save_project(self, id: UUID, project: Project, ppt_text: str) -> Project:
        pass


