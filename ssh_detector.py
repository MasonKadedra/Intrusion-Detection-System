#Kadedra Mason - 2304879

import re
from datetime import datetime, timedelta

Log_File = " /var/log/auth.log"
pattern = re.compile(r'(?P<timestamp>\w{3}\s+\d+\s[\d:]+).*Failed password for (invalid user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)')

def parse_timestamp(ts):
    return datetime.strptime(ts, "%b %d %H:%M:%S").replace(year=datetime.now().year)

def detect_bruteforceAttack():
    
    failed_attempt = {}
    alerts = []
    with open(Log_File, "r") as f:
        for line in f:
            
            match = pattern.search(line)
            if match:
                log_time = parse_timestamp(match.group ("timestamp"))
                ip = match.group("ip")
                user = match.group("user")
                
                if ip not in failed_attempts:
                    failed_attempts[ip] = []
                    
                    failed_attempts[ip].append((log_time, user))
                    
                    recents_attempts = [attempts for attempt in failed_attempts[ip]
                                        if log_time - attempt[0] <= timedelta(minutes = 2)]
                    
                    if len(recent_attempts) >= 5:
                        alerts.append({
                            "ip": ip,
                            "user": user,
                            "count": len(recent_attempts),
                            "time": log_time.strftime("%Y-%m-%d %H:%M:%S")
                            })
    return alerts

