import os
import subprocess

def open_app(query,say):
    apps = [
        ["notes", "open -a Notes"],
        ["facetime", "open -a facetime"],
        ["calendar", "open -a calendar"],
        ["weather app", "open -a weather"],
        ["whatsapp", "open -a WhatsApp"],
    ]

    for a in apps:
        if f"open {a[0].lower()}" in query.lower():
            say(f"Opening {a[0]} Abdullah..")
            os.system(a[1])
