#Kadedra Mason - 2304879

import re
from datetime import datetime, timedelta

#stores all ssh login attempts
Log_File = "/var/log/auth.log"

#converts timestamp string from log file into a date/time object for comparison
def parse_timestamp(ts):
    return datetime.fromisoformat(ts)

def detect_bruteforceAttack():
    failed_attempt = {}
    alerts = []

    #regex pattern that searches each log line, and extracts the important data
    pattern = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2}T[\d:.+-]+).*Failed password for (invalid user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)'
)

    with open(Log_File, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                log_time = parse_timestamp(match.group("timestamp"))
                ip = match.group("ip")
                user = match.group("user")

                if ip not in failed_attempt:
                    failed_attempt[ip] = []

                failed_attempt[ip].append((log_time, user))

                recent_attempts = [
                    attempt for attempt in failed_attempt[ip]
                    if log_time - attempt[0] <= timedelta(minutes=2)
                ]

                if len(recent_attempts) >= 5:
                    # Prevent duplicate alerts per IP
                    if not any(a['ip'] == ip for a in alerts):
                        alerts.append({
                            "ip": ip,
                            "user": user,
                            "count": len(recent_attempts),
                            "time": log_time.strftime("%Y-%m-%d %H:%M:%S")
                        })

    return alerts
