import youtube_dl

class Youtube():
    def __init__(self, savepath):
        self.savepath = savepath
        ydl_opts = {"outtmpl": "{}/%(title)s-%(id)s.%(ext)s".format(savepath)}
        self.ydl = youtube_dl.YoutubeDL(ydl_opts)

    def generate_metadata(self, url):
        info = self.ydl.extract_info(url, download=False)
        return {
            "name": info["title"],
            "duration": "{}s".format(info["duration"]),
            "description": info["description"],
            "upload_user": info["uploader"],
            "link": url
        }

    def download(self, link):
        self.ydl.download([link])
