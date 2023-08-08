import json
from y_tub_extractor import get_video_info,get_audio_url
from api_func import save_transcript

def save_video_sentiments(url):
    video_info = get_video_info(url)
    audio_info = get_audio_url(video_info)
    title = video_info["title"]
    title = title.strip().replace(" ", "_")
    title = "data/" + title
    save_transcript(audio_info,title,sentiment_analysis=True)

if __name__ == "__main__":
    save_video_sentiments("https://www.youtube.com/watch?v=BakfzsWv55A")