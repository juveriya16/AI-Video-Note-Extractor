import yt_dlp

def download_youtube_video(url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'uploads/youtube_video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename