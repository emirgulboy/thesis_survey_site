import abc


class img_interface(abc.ABC):
    @abc.abstractmethod
    def get_classes(self):
        pass

    @abc.abstractmethod
    def get_paths(self):
        pass
