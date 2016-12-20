"""
    Email template parser
    Nick Sif 08/09/2016

    Reads email templates created for the spear phishing project and turns them
    into Python email templates that can be pumped through the email scripts that
    have already been written for this project.
"""

import os
import csv
from email_template import EmailTemplate
import email as emailer


# create the dictionary of participant names and associated UIDs
users_dictionary = dict()
with open("fullname_uid.csv") as users_file:
    userlist_reader = csv.reader(users_file)
    for row in userlist_reader:
        users_dictionary[row[0].lower()] = row[1]


# generate a list of filenames in the raw_spears directory
# and create a dictionary associating that file with a UID
# if a name match can't be found, dump the file name to the screen and force the user to repair it
file_list = dict()
for file in os.listdir("raw_spears"):
    if file.endswith(".txt"):
        file_fullname = file.split(".")[0].lower()
        if file_fullname in users_dictionary:
            file_list[users_dictionary[file_fullname]] = "raw_spears/" + file
        else:
            print("No match found for " + file_fullname)


# parse each file! And extract some interesting data before any emails can be sent out
master_histogram = dict()
uid_template_map = dict()

for UID in file_list.keys():
    my_email = EmailTemplate(UID)
    try:
        with open(file_list[UID], encoding="utf-8-sig") as input_file:
            raw_data = input_file.readlines()
            for line in raw_data:
                line = line.strip()
                if "From" in line:
                    my_email.set_from(line)
                elif "Subject:" in line:
                    my_email.set_subject(line)
                elif line:
                    my_email.append_body(line)
    except:
        print("Caught an exception on UID " + UID + ", file " + file_list[UID])

    if not (my_email.from_address.lower(), my_email.subject_line.lower()) in master_histogram:
        master_histogram[(my_email.from_address.lower(), my_email.subject_line.lower())] = my_email

    uid_template_map[UID] = master_histogram[(my_email.from_address.lower(), my_email.subject_line.lower())].filename

with open("uid_template.csv", "w") as output_csv:
    for key, value in uid_template_map.items():
        output_csv.write(key + ", " + value + "\n")


# for key, value in master_histogram.items():
#     value.print_self()

    # my_email.print_self()
        # emailer.send_email(UID, "u5809912@anu.edu.au", "output/" + UID + ".txt")
