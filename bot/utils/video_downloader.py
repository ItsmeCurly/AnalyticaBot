from multiprocessing import Process
import youtube_dl
import moviepy.editor as mp
import os
import pytube


def download_yt_video(video_name: str) -> None:
    video = 'https://www.youtube.com/watch?v=lI5m0-oc9lI'
    
    pytube.YouTube('https://www.youtube.com/watch?v=lI5m0-oc9lI').streams.first().download(output_path='music', filename=f'video{video_name}')

    print(pytube.YouTube(video).streams.filter(only_audio=True).first().download())
        
    clip = mp.VideoFileClip(f"music\\video{video_name}.mp4").subclip(0, 10)
    clip.audio.write_audiofile(f"music\\video{video_name}.mp3")

if __name__ == "__main__":
    download_yt_video('a')
    #p = Process(target=download_yt_video, args=('a',))
    #p1 = Process(target=download_yt_video, args=('b',))
    #p.start()
    #p1.start()
    #p.join()


# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())


# def f(name):
#     info('function f')
#     print('hello', name)


# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
