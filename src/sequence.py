from sortedcontainers import SortedList


class SeqFunctions:

    @staticmethod
    def add(payload, elem, id):
        payload.add((elem, id))

        return payload

    @staticmethod
    def remove(payload, id):
        payload.add(id)

        return payload

    @staticmethod
    def merge(payload1, payload2):

        for item in payload2:
            if item not in payload1:
                payload1.add(item)

        return payload1

    @staticmethod
    def display(name, payload):

        print("{}: ".format(name), payload)

    @staticmethod
    def get_seq(payload):

        seq = ""
        for elem in payload:
            seq += elem
        return seq


class Sequence:

    def __init__(self, id):
        self.elem_list = SortedList()
        self.id_remv_list = SortedList()
        self.id_seq = SortedList()
        self.elem_seq = []
        self.id = id
        self.seqf = SeqFunctions()

    def update_seq(self):
        for item in self.elem_list:
            if item[1] not in self.id_remv_list and item[1] not in self.id_seq:
                self.id_seq.add(item[1])
        for id in self.id_remv_list:
            if id in self.id_seq:
                del self.elem_seq[self.id_seq.index(id)]
                self.id_seq.remove(id)

        for id in self.id_seq:
            for item in self.elem_list:
                if item[1] == id:
                    if len(self.elem_seq) > self.id_seq.index(id):
                        if item[0] != self.elem_seq[self.id_seq.index(id)]:
                            self.elem_seq.insert(self.id_seq.index(id),
                                                 item[0])
                    else:
                        self.elem_seq.append(item[0])

    def add(self, elem, id):

        self.elem_list = self.seqf.add(self.elem_list, elem, id)

        # Call update_seq function
        self.update_seq()

    def remove(self, id):

        self.id_remv_list = self.seqf.remove(self.id_remv_list, id)

        # Call update_seq function
        self.update_seq()

    def query(self, id):

        for item in self.elem_list:
            if item[1] == id:
                if id not in self.id_remv_list:
                    return True
                else:
                    return False
        return False

    def merge(self, list, func='na'):

        if func == 'na':
            self.elem_list = self.seqf.merge(self.elem_list, list.elem_list)
            self.id_remv_list = self.seqf.merge(self.id_remv_list,
                                                list.id_remv_list)
        elif func == 'elem':
            self.elem_list = self.seqf.merge(self.elem_list, list)
        elif func == 'id':
            self.id_remv_list = self.seqf.merge(self.id_remv_list, list)
        self.update_seq()

    def display(self):

        self.seqf.display("Elem List", self.elem_list)
        self.seqf.display("ID Removed List", self.id_remv_list)
        self.seqf.display("ID Seq", self.id_seq)
        self.seqf.display("Elem Seq", self.elem_seq)

    def get_seq(self):

        return self.seqf.get_seq(self.elem_seq)
