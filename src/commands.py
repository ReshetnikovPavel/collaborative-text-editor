import abc


class Command(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self):
        pass


class InsertCommand(Command):
    def __init__(self, crdt, char, position):
        self.crdt = crdt
        self.char = char
        self.position = position

    def execute(self):
        self.crdt.insert(self.char, self.position)


class RemoveCommand(Command):
    def __init__(self, crdt, position):
        self.crdt = crdt
        self.position = position

    def execute(self):
        self.crdt.remove(self.position)


class MergeCommand(Command):
    def __init__(self, crdt, other_crdt):
        self.crdt = crdt
        self.other_crdt = other_crdt

    def execute(self):
        self.crdt.merge(self.other_crdt)