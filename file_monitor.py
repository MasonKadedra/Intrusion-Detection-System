# Name: Monica Foreshaw
# ID: 2104888

import os
import hashlib
import json

# CONFIGURATION
#MONITOR_DIR = "C:/test_monitor"  #Testing-PyCharm
MONITOR_DIR = "/var/www"  #monitoring 1 Directory -Ubuntu
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


def file_checking():
    """Compare current files with baseline and return changes"""
    if not os.path.exists(HASH_FILE):
        print("Baseline not found! Creating baseline now...")
        creating_baseline()
        print("Baseline created. Run file check again to see changes.")
        return [], [], []

    with open(HASH_FILE, "r") as hash_data:
        saved_baseline = json.load(hash_data)

    recent_hashes = {}
    modified_files = []
    new_files = []
    deleted_files = []

    # Scan current files
    for root, dirs, files in os.walk(MONITOR_DIR):
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))
            current_hash = hash_calculation(file_path)
            if current_hash is None:
                continue  # skip unreadable files
            recent_hashes[file_path] = current_hash

            if file_path in saved_baseline:
                if saved_baseline[file_path] != current_hash:
                    modified_files.append(file_path)
            else:
                new_files.append(file_path)

    # Detect deleted files
    for file_path in saved_baseline:
        if file_path not in recent_hashes:
            deleted_files.append(file_path)

    return modified_files, new_files, deleted_files

