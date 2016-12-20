
"""
    Email template class

    Nick Sif 08/09/2016

    A class to hold all the data and things for an email.
"""


class EmailTemplate:

    def __init__(self, UID):
        self.from_address = ""
        self.from_from = ""
        self.subject_line = ""
        self.filename = "output/" + UID + ".txt"
        self.body = []

    """
        Extract the address that the email needs to appear to be from.
        There are two versions of this that's required - the from in the FROM
        statement, and the from in the DATA

        Build both of them in this function hey.
    """
    def set_from(self, from_string):
        parts = from_string.split("From: ")
        self.from_address = parts[1]

        parts = self.from_address.split(" ")
        self.from_from = "".join(parts)

    """
        Extract the subject line from the raw data.
    """
    def set_subject(self, subject_string):
        parts = subject_string.split("Subject: ")
        self.subject_line = parts[1]

    def append_body (self, body_string):
        self.body.append(body_string)

    def print_self(self):
        with open(self.filename, "w") as output_file:
            output_file.write(self.from_from + "\n")
            output_file.write(self.from_address + "\n")
            output_file.write(self.subject_line + "\n")
            for line in self.body:
                output_file.write("<p>" + line + "</p>\n")

    def load_self(self):
        with open(self.filename) as input_file:
            self.from_from = input_file.readline().strip()
            self.from_address = input_file.readline().strip()
            self.subject_line = input_file.readline().strip()
            for line in input_file:
                self.body.append(line.strip())
