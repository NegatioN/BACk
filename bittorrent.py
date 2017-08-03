import subprocess
import libtorrent as lt
import tempfile
import shutil
import sys
from time import sleep



class Bittorrent():
    def __init__(self):
        self.ses = lt.session()

    def generate_metadata(self, magnet):
        tempdir = tempfile.mkdtemp()
        params = {
            'save_path': tempdir,
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True
        }
        handle = lt.add_magnet_uri(self.ses, magnet, params)

        print("Downloading Metadata (this may take a while)")
        while (not handle.has_metadata()):
            try:
                sleep(1)
            except KeyboardInterrupt:
                print("Aborting...")
                self.ses.pause()
                print("Cleanup dir " + tempdir)
                shutil.rmtree(tempdir)
                sys.exit(0)
        self.ses.pause()
        print("Done")
        torinfo = handle.get_torrent_info()
        return torinfo

    def download_magnetfiles(self):
        pass
