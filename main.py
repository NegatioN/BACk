import subprocess
import bittorrent
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest="input", default="imagined_input_file.txt", help='Input-file with list of links')
parser.add_argument('--savepath', dest="savepath", default=".", help='Path to save all data in.')
parser.add_argument('--metadata', dest="metadata", default="metadata.lock", help='Target file for the metadata.')
config = parser.parse_args()


def metadata_exists(magnet, data_file):
    with open(data_file, "r") as lockfile:
        data = json.load(lockfile)
        for entry in data:
            if entry['magnet'] == magnet:
                return True
        return False


def add_metadata(metadata_entry, data_file):
    with open(data_file, "r") as lockfile:
        data = json.load(lockfile)
        data.append(metadata_entry)
    with open(data_file, "w") as lockfile:
        json.dump(data, lockfile, indent=4, sort_keys=True)


def main():
    metadata_path = config.metadata
    if not os.path.isfile(metadata_path):
        with open(metadata_path, "w") as lockfile:
            json.dump([], lockfile)
    bt = bittorrent.Bittorrent(config.savepath)
    with open(config.input, "r") as input_file:
        for line in input_file:
            name = line.strip()
            if name.startswith("magnet:"):
                if not metadata_exists(name, metadata_path):
                    add_metadata(bt.generate_metadata(name), config.metadata)
                bt.download_magnetfiles(name)
    #TODO ensure yt-cli and bt-cli in place
    #TODO backup metadata in a metadata.lock-file of some sort.
        #When does this happen? Don't kill entries when they are no longer accesible for example.
    #TODO execute download of a given storage-definition file.



if __name__ == "__main__":
    main()