from sortedcontainers import SortedSet

from src.position_generator import Position


class Sequence:

    def __init__(self, site_id: int):
        self.elements_with_ids = SortedSet()
        self.ids_to_remove = SortedSet()
        self.ids = SortedSet()
        self.elements = []
        self.site_id = site_id

    def to_string(self):
        return ''.join(self.elements)

    def add(self, element: chr, id: Position):
        self.elements_with_ids.add((element, id))
        self.update_sequence()

    def remove(self, id: Position):
        self.ids_to_remove.add(id)
        self.update_sequence()

    def contains_id(self, id_to_check: Position) -> bool:
        return id_to_check in map(lambda pair: pair[1], self.elements_with_ids) \
               and id_to_check not in self.ids_to_remove

    def merge(self, other: 'Sequence'):
        self.elements_with_ids = self.elements_with_ids.union(other.elements_with_ids)
        self.ids_to_remove = self.ids_to_remove.union(other.ids_to_remove)
        self.update_sequence()

    def update_sequence(self):
        self._add_ids()
        self._remove_ids_and_elements()
        self._add_new_elements()

    def _add_ids(self):
        for element, id in self.elements_with_ids:
            if id not in self.ids_to_remove and id not in self.ids:
                self.ids.add(id)

    def _remove_ids_and_elements(self):
        for id in self.ids_to_remove:
            if id in self.ids:
                del self.elements[self.ids.index(id)]
                self.ids.remove(id)

    def _add_new_elements(self):
        for id in self.ids:
            for item in self.elements_with_ids:
                if item[1] == id:
                    if len(self.elements) > self.ids.index(id):
                        if item[0] != self.elements[self.ids.index(id)]:
                            self.elements.insert(self.ids.index(id), item[0])
                    else:
                        self.elements.append(item[0])
