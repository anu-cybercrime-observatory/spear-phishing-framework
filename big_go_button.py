
from participant import Participant
import email as em
import email_template
import os


# GLOBAL VARIABLES
#
# MODIFY THESE AT YOUR OWN RISK
# THESE ARE THE GO BUTTONS

# Sandbox mode - testing the infrastructure, no emails will be sent.
sandbox = False
# Override the destination email addresses. Clearly for testing the emails before dispatch
override_email_addresses = False
override_email = ""
# Restrict the test run to this list of UIDs. (useful for localised testing)
restrict_UID = False
restrict_UID_list = []
# Save the email dispatch event to the database. Development mode = False
save_database_record = True


# Load up the email templates from the files.
templates = dict()
for file in os.listdir("output"):
    uid = file.split(".")[0]
    email = email_template.EmailTemplate(uid)
    email.load_self()
    templates[uid] = email


# load the table of participants
participants = []
with open("master.csv") as master_file:
    for line in master_file:
        newbie = Participant()
        newbie.from_string(line)
        participants.append(newbie)


# Load up the list of victims.
for participant in participants:
    uid = participant.uid

    if not restrict_UID or uid in restrict_UID_list:
        print("Processing %s" % uid)
        if not sandbox:
            destination_email = override_email if override_email_addresses else uid + "@anu.edu.au"
            em.send_email(participant, destination_email)

            # log the successful transmission of the email into the system database.
            if save_database_record:
                print("Logging %s to database" % uid)
                os.system("php ~/public/html/log_email_sent.php " + str(participant.anon_id))
