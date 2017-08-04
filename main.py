import bittorrent
import json
import os
import argparse
import youtube_dl

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest="input", default="imagined_input_file.txt", help='Input-file with list of links')
parser.add_argument('--savepath', dest="savepath", default=".", help='Path to save all data in.')
parser.add_argument('--metadata', dest="metadata", default="metadata.lock", help='Target file for the metadata.')
parser.add_argument('--do-download', dest="do_download", action="store_true",
                    help='Download all specified files. If not active, only generates metadata-file')
config = parser.parse_args()


def metadata_exists(magnet, data_file):
    with open(data_file, "r") as lockfile:
        data = json.load(lockfile)
        for entry in data:
            if entry['link'] == magnet:
                return True
        return False


def add_metadata(metadata_entry, data_file):
    with open(data_file, "r") as lockfile:
        data = json.load(lockfile)
        data.append(metadata_entry)
    with open(data_file, "w") as lockfile:
        json.dump(data, lockfile, indent=4, sort_keys=True)


# TODO consolidate metadata into a better common format?
def youtube_metadata(ydl, url):
    info = ydl.extract_info(url, download=False)
    return {
        "name": info["title"],
        "duration": "{}s".format(info["duration"]),
        "description": info["description"],
        "upload_user": info["uploader"],
        "link": url
    }


def main():
    metadata_path = config.metadata
    if not os.path.isfile(metadata_path):
        with open(metadata_path, "w") as lockfile:
            json.dump([], lockfile)

    if not os.path.isdir(config.savepath):
        os.mkdir(config.savepath)
    bt = bittorrent.Bittorrent(config.savepath)
    ydl_opts = {"outtmpl": "{}/%(title)s-%(id)s.%(ext)s".format(config.savepath)}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with open(config.input, "r") as input_file:
        for line in input_file:
            name = line.strip()
            if name.startswith("magnet:"):
                if not metadata_exists(name, metadata_path):
                    add_metadata(bt.generate_metadata(name), metadata_path)
                if config.do_download:
                    bt.download_magnetfiles(name)
            elif name.startswith("https://www.youtube"):
                if not metadata_exists(name, metadata_path):
                    add_metadata(youtube_metadata(ydl, name), metadata_path)
                if config.do_download:
                    ydl.download([name])


if __name__ == "__main__":
    main()