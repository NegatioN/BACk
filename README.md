# StorageAsCode
Made because I want an easy way to define whichever videos I feel are worth saving.
This is primarily a backup to easily re-download something if my local copies of the material gets destroyed.

## Usage
You should define a file with magnet-links or youtube-links to whatever you want to back up,
and this tool will generate a handy metadata-file so that even if the magnets or links you add die,
you can find it again.

After metadata is generated, the tool should download all of the data in the links provided.

`python main.py --input input_file.txt`

## Installation
Only tested with python 2.7
run `./installer.sh`