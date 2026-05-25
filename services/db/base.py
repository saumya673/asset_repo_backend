from abc import ABC, abstractmethod
from models import Project


class DBClient(ABC):
    @abstractmethod
    def get_projects(self, page_num: int, page_size: int) -> list[Project]:
        pass


