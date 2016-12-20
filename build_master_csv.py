
import csv
from participant import Participant

# Build the master CSV file which associates UID, ANON_ID, FIRST_NAME, FULL_NAME, and TEMPLATE_FILE
participants = dict()

with open("anonymiser.csv") as anon_file:
    records = csv.reader(anon_file.readlines())
    for uid, anon_id in records:
        uid = uid.strip()
        newbie = Participant()
        newbie.anon_id = anon_id.strip()
        newbie.uid = uid

        participants[uid] = newbie


with open("uid_template.csv") as template_file:
    records = csv.reader(template_file.readlines())
    for uid, template in records:
        uid = uid.strip()
        if uid in participants:
            participants[uid].template = template.strip()


with open("fullname_uid.csv") as template_file:
    records = csv.reader(template_file.readlines())
    for full_name, uid in records:
        uid = uid.strip()
        if __name__ == '__main__':
            if uid in participants:
                participants[uid].full_name = full_name
                participants[uid].first_name = full_name.split(" ")[0]


# participants is now containing the full set of data we want, so chuck in into the master CSV file
with open("master.csv", "w") as output_file:
    for participant in participants.values():
        output_file.write(participant.to_string() + "\n")
