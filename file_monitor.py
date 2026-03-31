# Name: Monica Foreshaw
# ID: 2104888

import os
import hashlib
import json

# CONFIGURATION
#MONITOR_DIR = "C:/test_monitor"  #Testing-PyCharm
MONITOR_DIR = "/var/www"  #monitoring 1 Directory -Kali
HASH_FILE = "hashing_files.json"  #baseline hashes save in file

def hash_calculation(file_location):  #Creates a function name hash_calculation that input the file path

    #This is the calculation of SHA-256 hash of a file.
    # it returns the hash as a hexadecimal string.
    hasher = hashlib.sha256()  #Creates a new SHA-256 calculator
    try:
        with open(file_location, "rb") as data_file:  #Opens the file at file_location and rb is read in binary mode
            #Read file in chunks to handle large files
            for block in iter(lambda: data_file.read(4096),
                              b""):  #Reads file in 4096 byte chunks at a time and until the file is read
                hasher.update(block)
        return hasher.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None  #If no file found or if there is no permission return none


def creating_baseline():  #Creates a function called creation_baseline
    #Scan all files in the monitoring directory and save their SHA-256 hashes
    #This is run the first time to take snapshot of all files

    snapshot_file = {}  #Creates an empty dictionary to store file paths and their hashes

    for root, dirs, files in os.walk(MONITOR_DIR):  #Goes through every folder and file in MONITOR_DIR
        for file in files:  #Loops through every file found
            file_path = os.path.normpath(os.path.join(root, file))#Builds full path of file
            snapshot_file[file_path] = hash_calculation(file_path)  #Stores hash in dictionary

    # Save baseline to JSON file
    with open(HASH_FILE, "w", encoding="utf-8") as baseline_file:  # Opens HASH_FILE to save hashes
        json.dump(snapshot_file, baseline_file, indent=4)  # Saves all hashes neatly to JSON

    print(f"[INFO] Baseline saved for {len(snapshot_file)} files.")  #Prints how many files saved


def file_checking():  #Creates a function called file_checking
    #Compare the current state of files with the baseline and detect:
    #modified files, deleted files and new files

    #Check if baseline exists; if not, create it automatically
    if not os.path.exists(HASH_FILE):  #Checks if baseline file exists
        print("Baseline not found!! Creating baseline now...")
        creating_baseline()  #calls creating_baseline to create it
        print(" Baseline created. Run the script again to check for changes.")  #statement printed if its created
        return  # Stops function after creating baseline

    #Load baseline hashes from file
    with open(HASH_FILE, "r") as hash_data:  #Opens saved baseline file
        saved_baseline = json.load(hash_data)  #Loads saved hashes into saved_baseline

        # Dictionaries and lists to track current hashes and changes
    recent_hashes = {}
    modify_files = []  #Files whose hash is modify, add here.
    new_files = []  #Files not in baseline add to new_files
    delete_files = []  #Files in baseline but missing now add to delete_files

    #Scan current files in the directory
    for root, dirs, files in os.walk(MONITOR_DIR):  #Goes through every folder in MONITOR_DIR
        for file in files:  #Loops through every file found
            file_scan = os.path.normpath(os.path.join(root, file))#Builds full path of file
            recent_hashes[file_scan] = hash_calculation(file_scan)  #Gets current hash of file

            # Check for modified files
            if file_scan in saved_baseline:  # If file exists in baseline
                if saved_baseline[file_scan] != recent_hashes[file_scan]:
                    modify_files.append(file_scan)  # Add to modified list
            else:
                # File is new not in baseline
                new_files.append(file_scan)  # Add file to new files list

    # Finding deleted files
    for file_scan in saved_baseline:  #Goes through every file in baseline
        if file_scan not in recent_hashes:  #If the file don't exist
            delete_files.append(file_scan)  #Add it to deleted list

    # OUTPUT STATEMENTS THAT DOES ALERT
    if modify_files or new_files or delete_files:

        if modify_files:
            print("\n[Note] Modified files are detected:")
            for file_found in modify_files:
               print(f"  - {file_found}")  #Prints each modified file
        if new_files:
            print("\n[Note] New files are detected:")
            for file_found in new_files:
                print(f"  - {file_found}")  #Prints each new file

        if delete_files:
            print("\n[Note] Delete Files detected:")
            for file_found in delete_files:
                print(f"  - {file_found}")  #Prints each deleted file
    else:

        print("[NOTE] No file changes were detected. All files are fine.")


# MENU
if __name__ == "__main__":
    print("=" * 50)  # Print 50 =
    print("WELCOME!!")
    print("File Integrity Monitor for IslandPay HID System")
    print("=" * 50)  # Print 50 =
    while True: #Will keep running until the user exits
            print("A. Baseline Creation")
            print("B. Check if any changes are made")
            print("C. Exit the menu")
            option = input("Select between A,B or C: ")

            if option == "A":  #If option A is selected then baseline is created
                creating_baseline() #Runs baseline creation
            elif option == "B":  #If option B is selected then check for changes
                file_checking()  #Runs file checking
            elif option == "C": #if selected it stops the loop
                print("GOOD BYE!!, You just exit the File Integrity Monitor")
                break #stops the loop
            else:
                print(
                     " Your selection is invalid — select A, B or C")  # if user select an invalid option, this statement is printed
