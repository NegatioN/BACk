import libtorrent as lt
from libtorrent import session
import tempfile
import shutil
import sys
from time import sleep

state_str = ['queued', 'checking', 'downloading metadata', \
             'downloading', 'finished', 'seeding', 'allocating']

def generate_params(save_path):
    return {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }

class Bittorrent():
    def __init__(self, savepath):
        self.savepath = savepath

    def generate_metadata(self, magnet):
        tempdir = tempfile.mkdtemp()
        ses = lt.session()
        handle = lt.add_magnet_uri(ses, magnet, generate_params(tempdir))

        print("Downloading Metadata of {}".format(magnet))
        while not handle.has_metadata():
            try:
                sleep(1)
            except KeyboardInterrupt:
                print("Aborting...")
                session.pause(ses)
                print("Cleanup dir " + tempdir)
                shutil.rmtree(tempdir)
                sys.exit(0)
        session.pause(ses)
        print("Done")
        torinfo = handle.get_torrent_info()
        info_entry = {
            "trackers": [t.url for t in torinfo.trackers()],
            "name": torinfo.name(),
            "link": magnet,
            "files": [f.path for f in torinfo.files()],
            "num_files": torinfo.num_files()
        }
        return info_entry

    def download_magnetfiles(self, magnet):
        ses = lt.session()
        handle = lt.add_magnet_uri(ses, magnet, generate_params(self.savepath))

        while not handle.status().is_seeding:
            status = handle.status()
            print('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                  (status.progress * 100, status.download_rate / 1000, status.upload_rate / 1000, \
                   status.num_peers, state_str[status.state]))
            sleep(1)
        session.pause(ses)
