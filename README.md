# StorageAsCode
Made because I want an easy way to define whichever videos I feel are worth saving.
This is primarily a backup to easily re-download something if my local copies of the material gets destroyed.

## Usage
You should define a file with magnet-links or youtube-links to whatever you want to back up,
and this tool will generate a handy metadata-file so that even if the magnets or links you add die,
you can find it again.

After metadata is generated, the tool should download all of the data in the links provided.

`python main.py --input input_file.txt` to generate the metadata-file.

`python main.py --input input_file.txt --do-download` to download everything in the input-file.

## Example input-file
The input-file can be a combination of magnet- and youtube-links:
```
https://www.youtube.com/watch?v=a1zDuOPkMSw
magnet:?xt=urn:btih:3e59b9d870e7921dc42b366c70b99acdef609c09&dn=%5BRyuusei%5D+Clannad+%28BDRip+1080p+x264+AAC%29+%5Brich_jc%5D&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969
```

## Installation
run `./installer.sh`

Only tested with python 2.7 on Ubuntu 16.04
