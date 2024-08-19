from exchangelib import Credentials, Account, DELEGATE
import json

USERNAME = "WINDOMAIN\\yourusername"
PASSWORD = "yourpassword"
SMTP = "yourusername@example.com"
TOP = "toplevelname"

credentials = Credentials(username=USERNAME, password=PASSWORD)
my_account = Account(
    primary_smtp_address=SMTP,
    credentials=credentials,
    autodiscover=True,
    access_type=DELEGATE,
)


def build_hierarchy(TOP):
    hierarchy = []
    for i in my_account.protocol.expand_dl(TOP):
        if i.mailbox_type == "PublicDL":
            hierarchy.append(
                {
                    "name": i.name,
                    "email_address": i.email_address,
                    "mailbox_type": i.mailbox_type,
                    "children": build_hierarchy(i.email_address),
                }
            )
        else:
            hierarchy.append(
                {
                    "name": i.name,
                    "email_address": i.email_address,
                    "mailbox_type": i.mailbox_type,
                }
            )
    return hierarchy


hierarchy = build_hierarchy(TOP)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(
        hierarchy,
        f,
    )
