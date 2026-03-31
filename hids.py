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
    file_checking()

    # --------------------------
    # SSH BRUTE FORCE CHECK
    # --------------------------
    print("\n[Checking SSH Logs...]")
    alerts = detect_bruteforceAttack()

    for alert in alerts:
        print(f"[ALERT] SSH Brute Force from {alert['ip']}")

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
