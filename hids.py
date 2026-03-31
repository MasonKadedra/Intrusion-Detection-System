# ==============================
# IMPORT MODULES
# ==============================

from file_monitor import file_checking
from ssh_detector import detect_bruteforceAttack
from logger import log_event
from alert import send_alert

# ==============================
# MAIN SYSTEM FUNCTION
# ==============================

def run_hids():
    print("=" * 50)
    print(" HIDS SYSTEM RUNNING ")
    print("=" * 50)

    # --------------------------
    # FILE INTEGRITY CHECK
    # --------------------------
    print("\n[Checking File Integrity...]")

    result = file_checking()

    # Ensure function returns values
    if result:
        modified, new, deleted = result

        # Modified files
        for file in modified:
            print(f"[MODIFIED] {file}")
            log_event("File Modified", "Medium", file, "File hash mismatch detected")
            send_alert(f"Modified file: {file}")

        # New files
        for file in new:
            print(f"[NEW FILE] {file}")
            log_event("New File", "Low", file, "New file detected")
            send_alert(f"New file: {file}")

        # Deleted files
        for file in deleted:
            print(f"[DELETED] {file}")
            log_event("File Deleted", "High", file, "File removed from system")
            send_alert(f"Deleted file: {file}")

    else:
        print("[OK] No file changes detected.")

    # --------------------------
    # SSH BRUTE FORCE CHECK
    # --------------------------
    print("\n[Checking SSH Logs...]")

    alerts = detect_bruteforceAttack()

    seen_ips = set()  # Prevent duplicate alerts

    for alert in alerts:
        if alert["ip"] in seen_ips:
            continue

        seen_ips.add(alert["ip"])

        print(f"[SECURITY ALERT] SSH Brute Force detected from {alert['ip']}")

        # LOG EVENT
        log_event(
            "SSH Brute Force",
            "High",
            alert["ip"],
            f"{alert['count']} failed login attempts within 2 minutes"
        )

        # SEND ALERT
        send_alert(f"Brute force detected from {alert['ip']}")

    if not alerts:
        print("[OK] No SSH brute force detected.")

# ==============================
# RUN PROGRAM
# ==============================

if __name__ == "__main__":
    run_hids()
