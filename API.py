from abc import ABC, abstractmethod


class Api(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass