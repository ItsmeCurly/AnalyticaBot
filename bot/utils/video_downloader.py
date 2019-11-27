import os
import urllib.request as request
from multiprocessing import Process

import moviepy.editor as mp
import pytube
import youtube_dl
from bs4 import BeautifulSoup, SoupStrainer
import time

base_url = 'https://www.youtube.com/results?search_query='


class Downloader():
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.search_results = {}

    # def download_yt_video(self, search_query: str) -> None:
    #     pytube.YouTube('https://www.youtube.com/watch?v=lI5m0-oc9lI').streams.filter(
    #         only_audio=True).first().download(output_path='music', filename=f'{video_name}')

    #     # print(pytube.YouTube(video).streams.filter(only_audio=True).first().download())

    #     clip = mp.VideoFileClip(f"music\\video{video_name}.mp4").subclip(0, 10)
    #     clip.audio.write_audiofile(f"music\\video{video_name}.mp3")

    def search_vid(self, video_name: str):
        response = request.urlopen(base_url + video_name.replace(" ", "%20"))
        soup = BeautifulSoup(response, "html.parser")

        divs = soup.find_all("div", {"class": "yt-lockup-content"})
        for i in divs:
            href = i.find('a', href=True)
            self.search_results["https://www.youtube.com" +
                                href["href"]] = href.text


if __name__ == "__main__":
    d = Downloader(2)  # dummy variable as of now
    p = Process(target=d.search_vid, args=("mitis shattered",))
    p.start()
