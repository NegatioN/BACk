import subprocess
import bittorrent

input_file_name = "imagined_input_file.txt"


def main():
    bt = bittorrent.Bittorrent()
    with open(input_file_name, "r") as input_file:
        for line in input_file:
            print(line.strip())
            name = line.strip()
            if name.startswith("magnet:"):
                print(bt.generate_metadata(name))
    #TODO ensure yt-cli and bt-cli in place
    #TODO backup metadata in a metadata.lock-file of some sort.
        #When does this happen? Don't kill entries when they are no longer accesible for example.
    #TODO execute download of a given storage-definition file.
    pass


if __name__ == "__main__":
    main()