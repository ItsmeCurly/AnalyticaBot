import pytube

def download_yt_video(video_name: str) -> None:
    pytube.YouTube('https://www.youtube.com/watch?v=lI5m0-oc9lI').streams.first().download(output_path='music', filename='video.mp3')

download_yt_video('')
