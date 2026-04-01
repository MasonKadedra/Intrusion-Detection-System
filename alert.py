# Brandon Blake
#2202851

import subprocess

# PURPOSE: Sends a desktop notification when a threat is detected

def send_alert(message):
    try:
        # notify-send is a Linux tool used for pop-up notifications
        subprocess.run(["notify-send", "HIDS Alert", message])
    except:
        # fallback in case notification fails
        print("ALERT:", message)

