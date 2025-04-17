from abc import ABC, abstractmethod

class RepositorioBase(ABC):
    @abstractmethod
    def crear(self, objeto):
        pass

    @abstractmethod
    def obtener_por_id(self, id_):
        pass

    @abstractmethod
    def actualizar(self, objeto):
        pass

    @abstractmethod
    def eliminar(self, id_):
        pass

    @abstractmethod
    def obtener_todos(self, objeto):
        pass
