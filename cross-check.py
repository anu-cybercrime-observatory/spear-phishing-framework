
import csv
import os


saved_tuples = dict()
with open("uid_template.csv") as input_file:
    tuples = csv.reader(input_file.readlines())

    for tuple in tuples:
        uid = tuple[1].split("/")[1].split(".")[0]
        saved_tuples[tuple[0]] = uid

file_list = []
for file in os.listdir("output-bak"):
    if file.endswith(".txt"):
        uid = file.split(".")[0]
        file_list.append(uid)

# now that we have both, cross check one against the other.
for key, value in saved_tuples.items():
    if not value in file_list:
        # this means that the wrong template is associated with this UID
        # which is the right template? Interesting. Clearly, it's a
        # template that is both associated with this 'wrong' one, and
        # it's a template which exists.
        #
        # holy shit!
        if key in file_list:
            print("Replace " + value + " with " + key)

print(":)")
