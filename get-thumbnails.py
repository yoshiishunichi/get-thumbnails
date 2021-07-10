from apiclient.discovery import build
import urllib.request as req
import os

API_KEY = "【API_KEY】"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtuberName = "【youtuberの名前】"
channelId = "【channelId】"

def saveThumbnail(response, count):
  c = 0
  for result in response.get("items", []):
    c += 1
    print(result["snippet"]["title"])
    thumbnailUrl = result["snippet"]["thumbnails"]["default"]["url"]

    no = (count - 1) * 50 + c
    noStr = str(no)
    noStrZero = noStr.zfill(3)
    req.urlretrieve(thumbnailUrl, "./image/" + youtuberName + "/thumbnail-" + noStrZero + ".png")
    print("Saved: thumbnail-" + noStrZero)

def accessApi(nextPageToken):
  my_youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

  videos_response = my_youtube.search().list(
    part="snippet",
    channelId=channelId,
    maxResults=50,
    order="date",
    pageToken=nextPageToken
  ).execute()

  return videos_response

if __name__ == '__main__':
  os.makedirs("./image/" + youtuberName, exist_ok=True)
  count = 0
  nextPageToken = ""
  while count < 4:
    count += 1
    response = accessApi(nextPageToken)
    saveThumbnail(response, count)
    try:
      nextPageToken = response["nextPageToken"]
    except:
      break