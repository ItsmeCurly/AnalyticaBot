from multiprocessing import Process
import youtube_dl
import moviepy.editor as mp
import os
import pytube
from bs4 import BeautifulSoup

import urllib.request as request

base_url = 'https://www.youtube.com/results?search_query='
class Downloader():
    def __init__(self, max_workers: int):
        self.max_workers = max_workers

    def download_yt_video(self, video_name: str) -> None:
        pytube.YouTube('https://www.youtube.com/watch?v=lI5m0-oc9lI').streams.first().download(output_path='music', filename=f'video{video_name}')

        #print(pytube.YouTube(video).streams.filter(only_audio=True).first().download())

        clip = mp.VideoFileClip(f"music\\video{video_name}.mp4").subclip(0, 10)
        clip.audio.write_audiofile(f"music\\video{video_name}.mp3")

    def search_vid(self, video_name: str):
        response = request.urlopen(base_url + video_name.replace(" ", "%20"))

        soup = BeautifulSoup(response)
        divs = soup.find_all("div", { "class" : "yt-lockup-content"})

        for i in divs:
            href = i.find('a', href=True)
            print(href.text,  "\nhttps://www.youtube.com"+href['href'], '\n')

if __name__ == "__main__":
    d = Downloader(2)
    d.search_vid("mitis shattered")
