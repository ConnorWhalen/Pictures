import os
from pathlib import Path
import re
import subprocess
from threading import Thread, Event
from time import sleep
from urllib.request import urlretrieve, Request

import m3u8

# ---- download audio to disk ----
# CHUNK_COUNT = 282

# url_base = "https://assets.heavynfldb.ca/streams/mussorgsky"
# audio_folder = "mp3"
# filename = "playlist.m3u8"

# os.makedirs(audio_folder, exist_ok=True)

# def download_file(file_url: str, file_path: str):
#     if not Path(file_path).is_file():
#         print(f"Downloading {file_url} to {file_path}")
#         r = Request(file_url, headers={
#                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
#             })
#         urlretrieve(
#             r.full_url,
#             file_path
#         )
#     else:
#         print(f"{file_path} exists")

# download_file(f"{url_base}/{filename}", f"{audio_folder}/{filename}")

# for chunk in range(CHUNK_COUNT):
#     chunk_name = f"file{chunk}.mp3"
#     download_file(f"{url_base}/{chunk_name}", f"{audio_folder}/{chunk_name}")

# # www.classicals.de
# song_path = "mp3/playlist.m3u8"
# ---- ---------------------- ----

# www.classicals.de
SONG_PATH = "https://assets.heavynfldb.ca/streams/mussorgsky/playlist.m3u8"

class AudioPlayer:

    def __init__(self, song_path: str):
        self.song_pos = 0
        self.duration = 0
        self.thread = None
        self.exit_flag = Event()

        self.song_path = song_path
        
    
    def start(self, defer=0.0):
        self.thread = Thread(target=self._play_song, args=[self.song_path, defer, self.exit_flag])
        self.thread.start()
        return self.thread
    
    def get_pos(self):
        return self.song_pos
    
    def get_duration(self):
        return self.duration
    
    def terminate(self):
        self.exit_flag.set()

    def _play_song(self, song_path: str, defer: float, exit_flag: Event):
        """Play song with ffplay and update song_pos as it plays."""

        while defer > 0:
            sleep(1)
            if exit_flag.is_set():
                return
            defer -= 1

        playlist = m3u8.load(song_path)
        self.duration = sum([segment.duration for segment in playlist.segments])

        # Read ffplay version to determine if -extension_picky arg is needed
        ext_picky = False

        version_process = subprocess.Popen(
            ["ffplay", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        output = version_process.communicate()
        res = re.search(r"ffplay version ([0-9]*)\.([0-9]*).*", output[0])
        if len(res.groups()) < 2:
            print("Cannot read ffplay version")
        else:
            # print(f"ffplay version is: {res.group(1)}.{res.group(2)}")
            version = float(f"{res.group(1)}.{res.group(2)}")
            if version >= 7.1:
                ext_picky = True

        cmd = [
            "ffplay",
            "-allowed_extensions",
            "mp3",
            "-extension_picky",
            "0",
            "-nodisp",
            "-autoexit",
            song_path
        ]
        if ext_picky:
            cmd.insert(3, "-extension_picky")
            cmd.insert(4, "0")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        prev_pos = -1
        for line in process.stdout:
            if exit_flag.is_set():
                process.terminate()
                return

            if res := re.search(r" *(-?[0-9]*\.?[0-9]*).*M\-A:.*fd=.*aq=.*vq=.*sq=.*", line):
                try:
                    pos = float(res.group(1))
                except ValueError:
                    continue

                if pos >= 0 and int(pos) != prev_pos:
                    # print(f"POS: {int(pos)} / {int(self.duration)}")
                    prev_pos = int(pos)
                    self.song_pos = prev_pos


if __name__ == "__main__":
    player = AudioPlayer(SONG_PATH)
    t = player.start()
    while t.is_alive:
        print(f"Song pos: {player.get_pos()}")
        sleep(1)
