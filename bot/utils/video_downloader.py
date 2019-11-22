import youtube_dl
import moviepy.editor as mp
import os
import pytube


def download_yt_video(video_name: str) -> None:
    pytube.YouTube('https://www.youtube.com/watch?v=lI5m0-oc9lI').streams.first().download(output_path='music', filename='video')

    clip = mp.VideoFileClip("music\\video.mp4").subclip(0, 10)
    clip.audio.write_audiofile("music\\video.mp3")

download_yt_video('')
