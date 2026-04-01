from file_monitor import file_checking, creating_baseline, MONITOR_DIR
from ssh_detector import detect_bruteforceAttack
from logger import log_event
from alert import send_alert

def run_hids():
    print("=" * 50)
    print(" HIDS SYSTEM RUNNING ")
    print("=" * 50)

    seen_ips = set()  # Prevent duplicate SSH alerts in this session

    while True:
        # --------------------------
        # MENU OPTIONS
        # --------------------------
        print("\nMenu:")
        print("A. Create Baseline")
        print("B. Check File Integrity")
        print("C. Check SSH Logs for Brute Force")
        print("D. Exit HIDS")

        option = input("Select A, B, C, or D: ").upper()
        print("\n")

        if option == "A":
            creating_baseline()
        elif option == "B":
            modified, new, deleted = file_checking()
           
            # Log modified files
            for file in modified:
                log_event(
                    "File Modified",
                    "Medium",
                    file,
                    "File Hash Mismatch Detected"
                )
                send_alert(f"Modified File detected: {file}")
           
            # Log new files
            for file in new:
                log_event(
                    "New File",
                    "Low",
                    file,
                    "New file added to directory"
                )
                send_alert(f"New File detected: {file}")
           
            # Log deleted files
            for file in deleted:
                log_event(
                    "Deleted File",
                    "High",
                    file,
                    "File deleted from directory"
                )
                send_alert(f"Deleted File detected: {file}")
        elif option == "C":
            alerts = detect_bruteforceAttack()
            if not alerts:
                print("[OK] No SSH brute force detected.")
            for alert in alerts:
                ip = alert["ip"]
                if ip in seen_ips:
                    continue
                seen_ips.add(ip)
                log_event(  
                    "SSH Brute Force",
                    "High",
                    ip,
                    f"{alert['count']} failed login attempts for user {alert['user']} within 2 minutes"
                )
                send_alert(
                    f"SSH Brute Force Detected!\n"
                    f"IP: {ip}\n"
                    f"User: {alert['user']}\n"
                    f"Time: {alert['time']}\n"
                    f"Attempts: {alert['count']}"
                    )
        elif option == "D":
            print("Exiting HIDS. Goodbye!")
            break
        else:
            print("Invalid selection — choose A, B, C, or D")

if __name__ == "__main__":
    run_hids()

