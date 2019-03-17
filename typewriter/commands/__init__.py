from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def execute(client, message):
        pass


from ..render.command import RenderTemplate
