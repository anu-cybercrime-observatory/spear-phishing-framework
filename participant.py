"""

    A little construct that holds all the data relating to a participant in this experiment.

"""


class Participant:
    def __init__(self):
        self.uid = ""
        self.anon_id = 0
        self.first_name = ""
        self.full_name = ""
        self.template = ""

    def to_string(self):
        return self.uid + "," + str(self.anon_id) + "," + self.first_name + "," + self.full_name + "," + self.template

    def from_string(self, string):
        parts = string.strip().split(",")
        self.uid = parts[0]
        self.anon_id = int(parts[1])
        self.first_name = parts[2]
        self.full_name = parts[3]
        self.template = parts[4]
