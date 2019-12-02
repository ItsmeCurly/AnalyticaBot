import os
import urllib.request as request
from multiprocessing import Process

import moviepy.editor as mp
import pytube
import youtube_dl
from bs4 import BeautifulSoup, SoupStrainer
import time
from urllib.parse import quote

base_url = 'https://www.youtube.com/results?search_query='

class Downloader():
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.search_results = []

    # def download_yt_video(self, search_query: str, song_name, artists_name) -> None:
    #     print(search_query)
    #     pytube.YouTube(search_query).streams.first().download(output_path='music', filename=f'{song_name}')

    #     clip = mp.VideoFileClip(
    #         f"music\\{song_name}.mp4")
    #     clip.audio.write_audiofile(f"music\\{song_name}.mp3")

    async def search_vid(self, video_name: str, artist_name: str):
        response = request.urlopen(base_url + quote(artist_name.replace(
            " ", "+")) + "+" + quote(video_name.replace(" ", "+")))
        soup = BeautifulSoup(response, "html.parser")

        divs = soup.find_all("div", {"class": "yt-lockup-content"}, limit = 5)
        count = 0
        for i in divs:
            if count > 5:
                return
            href = i.find('a', href=True)
            self.search_results.append(("https://www.youtube.com" +
                                href["href"], href.text))
            count+=1
        return self.search_results


# Downloader(2).download_yt_video(
#     'https://www.youtube.com/watch?v=NrWD9zZKNE4', 'feel this good', 'maduk')
