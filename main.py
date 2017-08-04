import subprocess
import bittorrent
import json
import os
from pprint import pformat

input_file_name = "imagined_input_file.txt"
lockfile_name = "metadata.lock"


def metadata_exists(magnet):
    with open(lockfile_name, "r") as lockfile:
        data = json.load(lockfile)
        for entry in data:
            if entry['magnet'] == magnet:
                return True
        return False

def add_metadata(metadata_entry):
    with open(lockfile_name, "r") as lockfile:
        data = json.load(lockfile)
        data.append(metadata_entry)
    with open(lockfile_name, "w") as lockfile:
        json.dump(data, lockfile, indent=4, sort_keys=True)


def main():
    if not os.path.isfile(lockfile_name):
        with open(lockfile_name, "w") as lockfile:
            json.dump([], lockfile)
    bt = bittorrent.Bittorrent()
    with open(input_file_name, "r") as input_file:
        for line in input_file:
            print(line.strip())
            name = line.strip()
            if name.startswith("magnet:") and not metadata_exists(name):
                add_metadata(bt.generate_metadata(name))
    #TODO ensure yt-cli and bt-cli in place
    #TODO backup metadata in a metadata.lock-file of some sort.
        #When does this happen? Don't kill entries when they are no longer accesible for example.
    #TODO execute download of a given storage-definition file.



if __name__ == "__main__":
    main()