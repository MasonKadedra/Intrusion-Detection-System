# Brandon Blake
#2202851

import subprocess

# PURPOSE: Sends a desktop notification when a threat is detected

def send_alert(message):
    print("\n========== 🚨 HIDS ALERT 🚨 ==========")
    print(message)
    print("=====================================\n")
