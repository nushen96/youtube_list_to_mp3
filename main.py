import re
import youtube_dl
import requests
from bs4 import BeautifulSoup
import concurrent.futures

def download_video(video_url):
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = video_url,download=False
        )
        filename = f"videos/{video_info['title'].replace('/','-')}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        print(f"{filename} succesfully downloaded")
    except Exception as e:
        print(f"Error while downloading video {video_url}: {e}")

# My target page has a specific structure (list of links with pagination, each linking to an embedded video).
# Thus, your scraping function(s) will probably be different. But these might be helpful ;)
# def get_video_pages():
#     pages_links = []
#     URL = "[YOUR_URL]"
#     i = 0
#     while True:
#         if i == 0:
#             page = requests.get(URL)
#         else:
#             page = requests.get(f"{URL}/page/{i}")
#         if page.status_code != 200:
#             break
#         soup = BeautifulSoup(page.content, "html.parser")
#         list_elements = soup.find_all('li', class_="tie-video")
#         for l in list_elements:
#             pages_links.append(l.find('a')['href'])
#         i+=1
#     return pages_links

# def get_video_urls(video_pages):
#     video_urls = []
#     for page in video_pages:
#         r = requests.get(page)
#         soup = BeautifulSoup(r.content, "html.parser")
#         video_url = soup.find('iframe')['src'].split('?')[0].replace('embed/','watch?v=')
#         video_urls.append(video_url)
#     return video_urls

# def write_list_to_file(list_,filename):
#     with open(filename, 'w') as f:
#         f.write('\n'.join(list_))

def download_list(list_filepath):
    videos = []
    try:
        with open(list_filepath, 'r') as f:
            for line in f:
                videos.append(line.strip())
    except Exception as e:
        print(f"Couldn't open list of videos: {e}")
        return
    # -- Just in case you want to use threads. Youtube will block that tho :D
    # with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    #     executor.map(download_video,videos)
    for video in videos:
        download_video(video)

download_list("url_list.txt")